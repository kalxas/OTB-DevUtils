#!/bin/bash
# Script to automate the Orfeo Toolbox library packaging for Ubuntu.
#
# Copyright (C) 2010, 2011 CNES - Centre National d'Etudes Spatiales
# by Sebastien DINOT <sebastien.dinot@c-s.fr>
#
# Monteverdi OTB is distributed under the CeCILL license version 2. See files
# Licence_CeCILL_V2-en.txt (english version) or Licence_CeCILL_V2-fr.txt
# (french version) in 'Copyright' directory for details. This licenses are
# also available online:
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
# http://www.cecill.info/licences/Licence_CeCILL_V2-fr.txt


SCRIPT_VERSION="1.0"

if [ -z "$DEBFULLNAME" ]; then
  DEBFULLNAME="OTB Team"
fi

if [ -z "$DEBEMAIL" ]; then
  DEBEMAIL="contact@orfeo-toolbox.org"
fi

export DEBFULLNAME
export DEBEMAIL

TMPDIR=$(mktemp -d /tmp/monteverdi.XXXXXX)
DIRNAME=$(dirname $0)
if [ "${DIRNAME:0:1}" == "/" ] ; then
    CMDDIR=$DIRNAME
elif [ "${DIRNAME:0:1}" == "." ] ; then
    CMDDIR=$(pwd)/${DIRNAME:2}
else
    CMDDIR=$(pwd)/$DIRNAME
fi
DEBDIR=$CMDDIR/debian
DEFAULT_GPGKEYID=0xAEB3D22F


display_version ()
{
    cat <<EOF

make_ubuntu_packages.sh, version ${SCRIPT_VERSION}
Copyright (C) 2010, 2011 CNES (Centre National d'Etudes Spatiales)
by Sebastien DINOT <sebastien.dinot@c-s.fr>

EOF
}


display_help ()
{
    cat <<EOF

This script is used to automate the Monteverdi workshop packaging for
Ubuntu. Source packages are created in ${TMPDIR} directory.

Usage:
  ./make_ubuntu_packages.sh [options]

Options:
  -h            Display this short help message.

  -v            Display version and copyright informations.

  -d directory  Top directory of the local repository clone

  -r tag        Revision to extract ('tip', rev. number, tag name). By default,
                the last tagged version (after tip) is used.

  -m version    External version of the Monteverdi workshop (ex. 1.6.0).
                By default the last version in changelog.in is used.

  -o version    External version of the OTB library (ex. 3.8.0)

  -p version    Version of the package (ex. 2). Default is 1.

  -c message    Changelog message : using a custom changelog message will
                also overide the external version of Monteverdi

  -g id         GnuPG key id used for signing (default ${DEFAULT_GPGKEYID})

  -a archive    Use a source archive ('orig') instead of a local repository
                (-d) and a revision (-r). It can be used in case a previous
                version of the package is already on the ppa. The source
                archive won't be uploaded again.

Example:
  ./make_ubuntu_packages.sh -d ~/otb/src/Monteverdi -r 1551 -o 3.8-RC1 -m 1.6-RC1 -p 2

EOF
}


check_src_top_dir ()
{
    if [ -z "$topdir" ] ; then
        echo "*** ERROR: missing top directory of the Mercurial working copy (option -d)"
        echo "*** Use ./make_ubuntu_packages.sh -h to show command line syntax"
        exit 3
    fi
    if [ ! -d "$topdir" ] ; then
        echo "*** ERRROR: directory '$topdir' doesn't exist"
        exit 2
    fi
    if [ ! -d "$topdir/.hg" ] ; then
        echo "*** ERRROR: No Mercurial working copy found in '$topdir' directory"
        exit 2
    fi
    if [ "$(hg identify $topdir)" == "000000000000 tip" ] ; then
        echo "*** ERROR: Mercurial failed to identify a valid repository in '$topdir'"
        exit 2
    fi
    topdir=$( cd $topdir ; pwd )
}


check_src_revision ()
{
    olddir=`pwd`
    cd "$topdir"
    if [ -z "$revision" ] ; then
        revision=`hg tags | head -n 2 | tail -n 1 | awk '{print $1}'`
        echo "Using last tagged revision : $revision"
    else
        if ! hg log -r "$revision" &>/dev/null ; then
          echo "*** ERROR: Revision $revision unknown"
          exit 2
        fi
    fi
    cd "$olddir"
}


check_external_version ()
{
    if [ -z "$src_version_full" ] ; then
        src_version_full=$changelog_version
        echo "Using last version in changelog.in : $src_version_full"
    fi
    if [ "`echo $src_version_full | sed -e 's/^[0-9]\+\.[0-9]\+\(\.[0-9]\+\|-RC[0-9]\+\)$/OK/'`" != "OK" ] ; then
        echo "*** ERROR: Monteverdi full version ($src_version_full) has an unexpected format"
        exit 3
    fi
    if [ -z "$otb_version_full" ] ; then
        echo "*** ERROR: missing version number of OTB (option -o)"
        echo "*** Use ./make_ubuntu_packages.sh -h to show command line syntax"
        exit 3
    fi
    if [ "`echo $otb_version_full | sed -e 's/^[0-9]\+\.[0-9]\+\(\.[0-9]\+\|-RC[0-9]\+\)$/OK/'`" != "OK" ] ; then
        echo "*** ERROR: OTB full version ($otb_version_full) has an unexpected format"
        exit 3
    fi

    src_version_major=`echo $src_version_full | sed -e 's/^\([0-9]\+\)\..*$/\1/'`
    src_version_minor=`echo $src_version_full | sed -e 's/^[^\.]\+\.\([0-9]\+\)[\.-].*$/\1/'`
    src_version_patch=`echo $src_version_full | sed -e 's/^.*[\.-]\(\(RC\)\?[0-9]\+\)$/\1/'`

    otb_version_major=`echo $otb_version_full | sed -e 's/^\([0-9]\+\)\..*$/\1/'`
    otb_version_minor=`echo $otb_version_full | sed -e 's/^[^\.]\+\.\([0-9]\+\)[\.-].*$/\1/'`
    otb_version_patch=`echo $otb_version_full | sed -e 's/^.*[\.-]\(\(RC\)\?[0-9]\+\)$/\1/'`
    otb_version_soname="${otb_version_major}.${otb_version_minor}"
}


check_gpgkeyid ()
{
    if [ -z "$gpgkeyid" ] ; then
        gpgkeyid=$DEFAULT_GPGKEYID
    fi
    gpg --list-secret-keys $gpgkeyid &>/dev/null
    if [ "$?" -ne 0 ] ; then
        echo "*** ERROR: Secret part of the GnuPG key $gpgkeyid is unavailable, packages can't be signed"
        exit 4
    fi
}


check_src_archive ()
{
    if [ ! -f "$source_archive" ] ; then
        echo "*** ERROR: archive '$source_archive' doesn't exist"
        exit 2
    fi
    extract_cmd="tar -xf"
    if [ -n "$(echo "${source_archive}" | grep -E -e '\.tar\.gz$')" ] ; then
      extract_cmd="tar -xzf"
    fi
    if [ -n "$(echo "${source_archive}" | grep -E -e '\.tgz$')" ] ; then
      extract_cmd="tar -xzf"
    fi
    if [ -n "$(echo "${source_archive}" | grep -E -e '\.tar\.xz$')" ] ; then
      extract_cmd="tar -xJf"
    fi
    if [ -n "$(echo "${source_archive}" | grep -E -e '\.tar\.bz2$')" ] ; then
      extract_cmd="tar -xjf"
    fi
}


set_ubuntu_code_name ()
{
    case "$1" in
        "vivid" )
            ubuntu_codename="Vivid Vervet"
            ubuntu_version="15.04"
            ;;        
        "trusty" )
            ubuntu_codename="Trusty Tahr"
            ubuntu_version="14.04"
            ;;
        "saucy" )
            ubuntu_codename="Saucy Salamander"
            ubuntu_version="13.10"
            ;;
        "raring" )
            ubuntu_codename="Raring Ringtail"
            ubuntu_version="13.04"
            ;;
        "quantal" )
            ubuntu_codename="Quantal Quetzal"
            ubuntu_version="12.10"
            ;;
        "precise" )
            ubuntu_codename="Precise Pangolin"
            ubuntu_version="12.04"
            ;;
        "oneiric" )
            ubuntu_codename="Oneiric Ocelot"
            ubuntu_version="11.10"
            ;;
        "natty" )
            ubuntu_codename="Natty Narwhal"
            ubuntu_version="11.04"
            ;;
        "maverick" )
            ubuntu_codename="Maverick Meerkat"
            ubuntu_version="10.10"
            ;;
        "lucid" )
            ubuntu_codename="Lucid Lynx"
            ubuntu_version="10.04 LTS"
            ;;
        "karmic" )
            ubuntu_codename="Karmic Koala"
            ubuntu_version="9.10"
            ;;
        "hardy" )
            ubuntu_codename="Hardy Heron"
            ubuntu_version="08.04 LTS"
            ;;
        * )
            echo "*** ERROR: Unknown Ubuntu version name"
            exit 4
            ;;
    esac
}

pkg_version=1
# -sa : force original source inclusion
# -sd : force original source exclusion, only produce diff
include_src_option="-sa"

while getopts ":r:d:m:o:p:c:g:a:hv" option
do
    case $option in
        d ) topdir=$OPTARG
            ;;
        r ) revision=$OPTARG
            ;;
        m ) src_version_full=$OPTARG
            ;;
        o ) otb_version_full=$OPTARG
            ;;
        p ) pkg_version=$OPTARG
            ;;
        c ) changelog_message=$OPTARG
            ;;
        g ) gpgkeyid=$OPTARG
            ;;
        a ) source_archive=$OPTARG
            include_src_option="-sd"
            ;;
        v ) display_version
            exit 0
            ;;
        h ) display_help
            exit 0
            ;;
        * ) echo "*** ERROR: Unknown option -$OPTARG (arg #"$(($OPTIND - 1))")"
            display_help
            exit 0
            ;;
    esac
done

if [ "$OPTIND" -eq 1 ] ; then
    display_help
    exit 1
fi

# find last version in changelog.in
changelog_version=`grep monteverdi "$DEBDIR/changelog.in" | head -n 1 | cut -d '(' -f 2 | cut -d '-' -f 1`

echo "Command line checking..."
if [ -n "$source_archive" ] ; then
  echo "Using source archive"
  check_src_archive
else
  echo "Using local repository"
  check_src_top_dir
  check_src_revision
fi

check_external_version
check_gpgkeyid

if [ -n "$source_archive" ] ; then
  echo "Archive extraction..."
  cp "$source_archive" "$TMPDIR"
  cd "$TMPDIR"
  $extract_cmd `basename "$source_archive"`
else
  echo "Archive export..."
  cd "$topdir"
  hg archive -r "$revision" -t tgz "$TMPDIR/monteverdi-$src_version_full.tar.gz"

  echo "Archive extraction..."
  cd "$TMPDIR"
  tar xzf "monteverdi-$src_version_full.tar.gz"
  mv "monteverdi-$src_version_full.tar.gz" "monteverdi_$src_version_full.orig.tar.gz"
fi

echo "Debian scripts import..."
cd "$TMPDIR/monteverdi-$src_version_full"
cp -a "$DEBDIR" .

make -f debian/rules control-file OTB_VERSION_MINIMAL=$otb_version_full
rm -f debian/control.in

echo "Source package generation..."
for target in precise trusty vivid ; do
    set_ubuntu_code_name "$target"
    echo "Package for $ubuntu_codename ($ubuntu_version)"
    cp -f "$DEBDIR/changelog.in" debian
    make -f debian/rules changelog-file DIST=$target PKGVERSION=$pkg_version
    rm -f debian/changelog.in
    if [ -n "$changelog_message" ] ; then
        dch --force-distribution --distribution "$target" \
          -v "${src_version_full}-0ppa~${target}${pkg_version}" "$changelog_message"
    else
        if [ "${src_version_full}" != "${changelog_version}" ] ; then
           echo "*** ERROR: changelog version (${changelog_version}) differs from external version (${src_version_full})"
           echo "*** Use option (-c) to overide the changelog message and version"
           exit 1
        fi
    fi
    debuild -k$gpgkeyid -S $include_src_option --lintian-opts -i
done
