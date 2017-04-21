#!/bin/sh

############################################
# Install ffmpeg with gpu for ubuntu 16.04 #
############################################

WORK_FOLDER="$PWD"

#############################################
# Install the latest nvidia driver and cuda #
#############################################

add-apt-repository ppa:graphics-drivers/ppa
apt-get update
apt-get install nvidia-381 nvidia-381-dev -y
apt-get install nvidia-cuda-toolkit --install-recommends -y
# Warning, you need to reboot after this step !
read -p "Warning, you need to reboot after this step the first time ! Press a key to continue ..." val1

########################
# Install dependencies #
########################

# libs and tools
apt-get -y install autoconf automake build-essential libass-dev libtool \
pkg-config texinfo zlib1g-dev cmake-curses-gui
# nvenc dependencies
apt-get -y install glew-utils libglew-dbg libglew-dev libglew1.13 libglewmx-dev \
libglewmx-dbg freeglut3 freeglut3-dev freeglut3-dbg libghc-glut-dev \
libghc-glut-doc libghc-glut-prof libalut-dev libxmu-dev libxmu-headers libxmu6 \
libxmu6-dbg libxmuu-dev libxmuu1 libxmuu1-dbg
# yasm for optimization
apt-get install yasm

###########
# libx264 #
###########

cd "$WORK_FOLDER"
mkdir ffmpeg_sources
cd ffmpeg_sources
wget http://download.videolan.org/pub/x264/snapshots/last_x264.tar.bz2
tar xjvf last_x264.tar.bz2
cd x264-snapshot*
PATH="$WORK_FOLDER/ffmpeg_build/bin:$PATH" ./configure --prefix="$WORK_FOLDER/ffmpeg_build" --bindir="$WORK_FOLDER/ffmpeg_build/bin" --enable-static --disable-opencl
PATH="$WORK_FOLDER/ffmpeg_build/bin:$PATH" make -j88
make -j$(nproc) install
make -j$(nproc) distclean

##############
# libfdk-aac #
##############

cd "$WORK_FOLDER/ffmpeg_sources"
wget -O fdk-aac.tar.gz https://github.com/mstorsjo/fdk-aac/tarball/master
tar xzvf fdk-aac.tar.gz
cd mstorsjo-fdk-aac*
autoreconf -fiv
./configure --prefix="$WORK_FOLDER/ffmpeg_build" --disable-shared
make -j$(nproc)
make -j$(nproc) install
make -j$(nproc) distclean

#################
# NVENC 7.0 SDK #
#################

cd "$WORK_FOLDER"
wget -c https://github.com/jniltinho/oficinadotux/raw/master/ffmpeg_nvenc/Video_Codec_SDK_7.1.9.zip
unzip Video_Codec_SDK_7.1.9.zip
cp -vr Video_Codec_SDK_7.1.9/Samples/common/inc/GL/* /usr/include/GL/
cp -vr Video_Codec_SDK_7.1.9/Samples/common/inc/*.h /usr/include/
mv Video_Codec_SDK_7.1.9 "$WORK_FOLDER/ffmpeg_sources/nv_sdk"
rm -f Video_Codec_SDK_7.1.9.zip

##########
# Ffmpeg #
##########

cd "$WORK_FOLDER/ffmpeg_sources"
git clone https://github.com/FFmpeg/FFmpeg -b master
cd FFmpeg
PATH="$WORK_FOLDER/ffmpeg_build/bin:$PATH"
PKG_CONFIG_PATH="$WORK_FOLDER/ffmpeg_build/lib/pkgconfig" ./configure \
 --prefix="$WORK_FOLDER/ffmpeg_build" \
 --pkg-config-flags="--static" \
 --extra-cflags="-I$WORK_FOLDER/ffmpeg_build/include" \
 --extra-ldflags="-L$WORK_FOLDER/ffmpeg_build/lib" \
 --bindir="$WORK_FOLDER/ffmpeg_build/bin" \
 --enable-cuda \
 --enable-cuvid \
 --enable-libnpp \
 --extra-cflags=-I../nv_sdk \
 --extra-ldflags=-L../nv_sdk \
 --enable-gpl \
 --enable-libass \
 --enable-libfdk-aac \
 --enable-libx264 \
 --enable-nvenc \
 --enable-nonfree
PATH="$WORK_FOLDER/ffmpeg_build/bin:$PATH" make -j$(nproc)
make -j$(nproc) install
make -j$(nproc) distclean
hash -r

################
# qt-faststart #
################

cd "$WORK_FOLDER/ffmpeg_sources/FFmpeg/tools"
cc qt-faststart.c -o qt-faststart
cp qt-faststart "$WORK_FOLDER/ffmpeg_build/bin"

###########################
# Links to /usr/local/bin #
###########################

rm /usr/local/bin/x264 && ln -s "$WORK_FOLDER/ffmpeg_build/bin/x264" /usr/local/bin/x264
rm /usr/local/bin/qt-faststart && ln -s "$WORK_FOLDER/ffmpeg_build/bin/qt-faststart" /usr/local/bin/qt-faststart
rm /usr/local/bin/ffserver && ln -s "$WORK_FOLDER/ffmpeg_build/bin/ffserver" /usr/local/bin/ffserver
rm /usr/local/bin/ffprobe && ln -s "$WORK_FOLDER/ffmpeg_build/bin/ffprobe" /usr/local/bin/ffprobe
rm /usr/local/bin/ffmpeg && ln -s "$WORK_FOLDER/ffmpeg_build/bin/ffmpeg" /usr/local/bin/ffmpeg

##############
# Try ffmpeg #
##############

/usr/local/ffmpeg -h

# Usage example
# ffmpeg -hwaccel cuvid -c:v h264_cuvid -i input.mp4 -vf scale_npp=1280:720 -c:v h264_nvenc -profile:v main -pixel_format yuv444p -preset default -b:v 1024k -c:a libfdk_aac -ar 48000 -ac 2 -ab 192k -movflags faststart -y output.mp4
