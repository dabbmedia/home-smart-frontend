TARGET = home_smart_camera
# LIB_INCLUDES = -I/usr/include/gstreamer-1.0 -I/usr/include/glib-2.0 -I/usr/include/libxml2
# CFLAGS = -O0 -g3 -Wall -c -fmessage-length=0
PKG_CONF = `pkg-config --cflags --libs gstreamer-1.0 gobject-2.0 glib-2.0`

all: main.o
# 	gcc $(LIB_INCLUDES) $(CFLAGS) main.c -o $(TARGET) $(PKG_CONF)
	gcc main.c -o $(TARGET) $(PKG_CONF)

clean:
	-rm -f *.o
	-rm -f /tmp/jpg/*.jpg
	-rm -f $(TARGET)
