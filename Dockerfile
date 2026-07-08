FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME=/opt/android-sdk
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV ANDROID_NDK_HOME=/opt/android-sdk/ndk/26.3.11579264
ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/build-tools/33.0.2

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    openjdk-17-jdk git zip unzip wget \
    autoconf automake libtool libltdl-dev \
    libffi-dev libssl-dev cmake \
    libncurses5-dev libncursesw5-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 Android SDK
RUN mkdir -p $ANDROID_HOME/cmdline-tools \
    && cd $ANDROID_HOME/cmdline-tools \
    && wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip \
    && unzip -q commandlinetools-linux-11076708_latest.zip \
    && mv cmdline-tools latest \
    && rm commandlinetools-linux-11076708_latest.zip \
    && yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --sdk_root=$ANDROID_HOME --licenses \
    && $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --sdk_root=$ANDROID_HOME \
        "platform-tools" "platforms;android-33" "build-tools;33.0.2" "ndk;26.3.11579264"

# 安装 buildozer
RUN pip3 install buildozer cython

WORKDIR /app
COPY . .

# 创建 SDK 符号链接（buildozer 期望的路径）
RUN mkdir -p ~/.buildozer/android/platform/android-sdk \
    && ln -sf $ANDROID_HOME/build-tools ~/.buildozer/android/platform/android-sdk/build-tools \
    && ln -sf $ANDROID_HOME/platforms ~/.buildozer/android/platform/android-sdk/platforms \
    && ln -sf $ANDROID_HOME/platform-tools ~/.buildozer/android/platform/android-sdk/platform-tools \
    && ln -sf $ANDROID_HOME/cmdline-tools ~/.buildozer/android/platform/android-sdk/cmdline-tools \
    && mkdir -p ~/.buildozer/android/platform/android-sdk/tools/bin \
    && ln -sf $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager ~/.buildozer/android/platform/android-sdk/tools/bin/sdkmanager \
    && ln -sf $ANDROID_NDK_HOME ~/.buildozer/android/platform/android-ndk-r26b

CMD ["buildozer", "android", "debug"]
