# Install script for directory: /home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/coralmicro/libs

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "TRUE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/home/kate/Documents/MF2143/coralmicro/third_party/toolchain-linux/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-objdump")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/audio/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/CMSIS/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/camera/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/cdc_acm/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/cdc_eem/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/coremark/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/FreeRTOS/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/rpc/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/msc_ums/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/a71ch/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/base/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/curl/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/flatbuffers/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/gemmlowp/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/kissfft/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/libjpeg/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/littlefs/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/mjson/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/nxp/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/pmic/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/ruy/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/tensorflow/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/testlib/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/tpu/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/usb/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/kate/Documents/MF2143/MF2143-Project/firmware/object-detection-http/build/coralmicro/libs/arduino/cmake_install.cmake")
endif()

