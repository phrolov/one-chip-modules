Import('env')
# 8 MHz
env.Replace(FUSESCMD="$UPLOADER $UPLOADERFLAGS -e -Uefuse:w:0xff:m -Uhfuse:w:0xdf:m -Ulfuse:w:0xe2:m")
