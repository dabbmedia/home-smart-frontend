//
//  main.c
//  home_smart_camera_hls
//
//  Created by Brent Self on 5/13/20 from GStreamer Lesson 8.
// https://gstreamer.freedesktop.org/documentation/tutorials/basic/short-cutting-the-pipeline.html?gi-language=c
//  Copyright © 2020 Brent Self. All rights reserved.
//
#include <gst/gst.h>
#include <gst/audio/audio.h>
#include <string.h>

#define CHUNK_SIZE 1024   /* Amount of bytes we are sending in each buffer */
#define SAMPLE_RATE 44100 /* Samples per second we are sending */

/* Structure to contain all our information, so we can pass it to callbacks */
typedef struct _CameraData {
  GstElement *pipeline, *tee;
  GstElement *video_queue, *v4l2_source, *filter, *video_convert, *h264_encode, *h264_parse, *mpegts_mux, *hls_sink;
  GstElement *image_queue, *multifile_sink;
  GstElement *app_queue, *app_sink;
  
  GstCaps *filtercaps;

  guint64 num_samples;   /* Number of samples generated so far (for timestamp generation) */
  
  GString *test_string;

  guint sourceid;        /* To control the GSource */

  GMainLoop *main_loop;  /* GLib's Main Loop */
} CameraData;

/* This method is called by the idle GSource in the mainloop, to feed CHUNK_SIZE bytes into appsrc.
 * The idle handler is added to the mainloop when appsrc requests us to start sending data (need-data signal)
 * and is removed when appsrc has enough data (enough-data signal).
 */
static gboolean push_data (CameraData *data) {
  GstBuffer *buffer;
  GstFlowReturn ret;
//  int i;
//  GstMapInfo map;
//  gint16 *raw;
  gint num_samples = CHUNK_SIZE / 2; /* Because each sample is 16 bits */
//  gfloat freq;

  /* Create a new empty buffer */
  buffer = gst_buffer_new_and_alloc (CHUNK_SIZE);

  /* Set its timestamp and duration */
  GST_BUFFER_TIMESTAMP (buffer) = gst_util_uint64_scale (data->num_samples, GST_SECOND, SAMPLE_RATE);
  GST_BUFFER_DURATION (buffer) = gst_util_uint64_scale (num_samples, GST_SECOND, SAMPLE_RATE);

  /* Generate some psychodelic waveforms */
//  gst_buffer_map (buffer, &map, GST_MAP_WRITE);
//  raw = (gint16 *)map.data;
//  data->c += data->d;
//  data->d -= data->c / 1000;
//  freq = 1100 + 1000 * data->d;
//  for (i = 0; i < num_samples; i++) {
//    data->a += data->b;
//    data->b -= data->a / freq;
//    raw[i] = (gint16)(500 * data->a);
//  }
//  gst_buffer_unmap (buffer, &map);
//  data->num_samples += num_samples;

  /* Push the buffer into the appsrc */
//  g_signal_emit_by_name (data->app_source, "push-buffer", buffer, &ret);

  /* Free the buffer now that we are done with it */
//  gst_buffer_unref (buffer);

//  if (ret != GST_FLOW_OK) {
//    /* We got some error, stop sending data */
//    return FALSE;
//  }
//
  return TRUE;
}

/* This signal callback triggers when appsrc needs data. Here, we add an idle handler
 * to the mainloop to start pushing data into the appsrc */
static void start_feed (GstElement *source, guint size, CameraData *data) {
  if (data->sourceid == 0) {
    g_print ("Start feeding\n");
    data->sourceid = g_idle_add ((GSourceFunc) push_data, data);
  }
}

/* This callback triggers when appsrc has enough data and we can stop sending.
 * We remove the idle handler from the mainloop */
static void stop_feed (GstElement *source, CameraData *data) {
  if (data->sourceid != 0) {
    g_print ("Stop feeding\n");
    g_source_remove (data->sourceid);
    data->sourceid = 0;
  }
}

/* The appsink has received a buffer */
static GstFlowReturn new_sample (GstElement *sink, CameraData *data) {
  GstSample *sample;

  /* Retrieve the buffer */
  g_signal_emit_by_name (sink, "pull-sample", &sample);
  if (sample) {
    /* The only thing we do in this example is print a * to indicate a received buffer */
//    g_print ("*");
//    g_print("%s\n", data->test_string->str);
    gst_sample_unref (sample);
    return GST_FLOW_OK;
  }

  return GST_FLOW_ERROR;
}

//static void insert_record (GString *text_msg) {
//  try {
//     connection C("dbname = testdb user = postgres password = postgres \
//     hostaddr = 127.0.0.1 port = 5432");
//     if (C.is_open()) {
//        cout << "Opened database successfully: " << C.dbname() << endl;
//     } else {
//        cout << "Can't open database" << endl;
//        return 1;
//     }
//     C.disconnect ();
//  } catch (const std::exception &e) {
//     cerr << e.what() << std::endl;
//     return 1;
//  }
//}

/* This function is called when an error message is posted on the bus */
static void error_cb (GstBus *bus, GstMessage *msg, CameraData *data) {
  GError *err;
  gchar *debug_info;

  /* Print error details on the screen */
  gst_message_parse_error (msg, &err, &debug_info);
  g_printerr ("Error received from element %s: %s\n", GST_OBJECT_NAME (msg->src), err->message);
  g_printerr ("Debugging information: %s\n", debug_info ? debug_info : "none");
  g_clear_error (&err);
  g_free (debug_info);

  g_main_loop_quit (data->main_loop);
}

int main(int argc, char *argv[]) {
  g_print("my main main!!\n");
//  create still images directory, if it doesn't exist
  
  CameraData data;
  GstPad *tee_video_pad, *tee_image_pad, *tee_app_pad; //*tee_audio_pad,
  GstPad *queue_video_pad, *queue_image_pad, *queue_app_pad; //*queue_audio_pad,
//  GstAudioInfo info;
//  GstCaps *audio_caps;
  GstBus *bus;

  /* Initialize custom data structure */
  memset (&data, 0, sizeof (data));
//  data.b = 1; /* For waveform generation */
//  data.d = 1;

  /* Initialize GStreamer */
  gst_init (&argc, &argv);

  /* Create the elements */
//  data.test_string = g_string_new("testene");
//  data.app_source = gst_element_factory_make ("appsrc", "audio_source");
  data.tee = gst_element_factory_make ("tee", "tee");
//  data.audio_queue = gst_element_factory_make ("queue", "audio_queue");
//  data.audio_convert1 = gst_element_factory_make ("audioconvert", "audio_convert1");
//  data.audio_resample = gst_element_factory_make ("audioresample", "audio_resample");
//  data.audio_sink = gst_element_factory_make ("autoaudiosink", "audio_sink");
  data.video_queue = gst_element_factory_make ("queue", "video_queue");
//  data.audio_convert2 = gst_element_factory_make ("audioconvert", "audio_convert2");
//  data.visual = gst_element_factory_make ("wavescope", "visual");
  data.v4l2_source = gst_element_factory_make("v4l2src", "v4l2_source");
  g_object_set (data.v4l2_source, "device", "/dev/video0", NULL);
  
  data.filter = gst_element_factory_make ("capsfilter", "filter");
  data.filtercaps = gst_caps_new_simple ("video/x-raw",
//               "format", G_TYPE_STRING, "I420",
               "width", G_TYPE_INT, 640,
               "height", G_TYPE_INT, 480,
               "framerate", GST_TYPE_FRACTION, 25, 1,
               NULL);
  g_object_set (G_OBJECT (data.filter), "caps", data.filtercaps, NULL);
  gst_caps_unref (data.filtercaps);
  
  data.video_convert = gst_element_factory_make ("videoconvert", "video_convert");
  data.h264_encode = gst_element_factory_make ("omxh264enc", "h264_encode");
//  data.h264_encode = gst_element_factory_make ("v4l2h264enc", "h264_encode");
  
  data.h264_parse = gst_element_factory_make ("h264parse", "h264_parse");
  // required to play in safari, without only plays in VLC
  g_object_set (data.h264_parse, "config-interval", -1, NULL);
  
  data.mpegts_mux = gst_element_factory_make ("mpegtsmux", "mpegts_mux");
  
  //mkdir /tmp/hls, if it doesn't exist
  data.hls_sink = gst_element_factory_make ("hlssink", "hls_sink");
  g_object_set (data.hls_sink, "location", "/tmp/hls/segment%05d.ts", NULL);
  g_object_set (data.hls_sink, "playlist-location", "/tmp/hls/playlist.m3u8", NULL);
  g_object_set (data.hls_sink, "target-duration", 1, NULL);
  
  data.image_queue = gst_element_factory_make ("queue", "image_queue");
  data.multifile_sink = gst_element_factory_make ("multifilesink", "multifile_sink");
  g_object_set (data.multifile_sink, "max-files", 10860, NULL);
//  g_object_set (data.multifile_sink, "post-messages", true, NULL);
  g_object_set (data.multifile_sink, "location", "/tmp/jpg/frame-%08d.jpg", NULL);
  
  data.app_queue = gst_element_factory_make ("queue", "app_queue");
  data.app_sink = gst_element_factory_make ("appsink", "app_sink");

  /* Create the empty pipeline */
  data.pipeline = gst_pipeline_new ("test-pipeline");

  if (!data.pipeline) {
    g_printerr ("Pipeline element could not be created.\n");
    return -1;
  }
  if (!data.v4l2_source) {
    g_printerr ("v4l2_source element could not be created.\n");
    return -1;
  }
  if (!data.tee) {
    g_printerr ("tee element could not be created.\n");
    return -1;
  }
  if (!data.video_queue) {
    g_printerr ("video_queue element could not be created.\n");
    return -1;
  }
  if (!data.h264_encode) {
    g_printerr ("h264_encode element could not be created.\n");
    return -1;
  }
  if (!data.h264_parse) {
    g_printerr ("h264_parse element could not be created.\n");
    return -1;
  }
  if (!data.mpegts_mux) {
    g_printerr ("mpegts_mux element could not be created.\n");
    return -1;
  }
  if (!data.video_convert) {
    g_printerr ("video_convert element could not be created.\n");
    return -1;
  }
  if (!data.hls_sink) {
    g_printerr ("hls_sink element could not be created.\n");
    return -1;
  }
  if (!data.image_queue) {
    g_printerr ("image_queue element could not be created.\n");
    return -1;
  }
  if (!data.multifile_sink) {
    g_printerr ("multifile_sink element could not be created.\n");
    return -1;
  }
  if (!data.app_queue) {
    g_printerr ("app_queue element could not be created.\n");
    return -1;
  }
  if (!data.app_sink) {
    g_printerr ("app_sink element could not be created.\n");
    return -1;
  }
//  if (!data.pipeline || !data.v4l2_source || !data.tee || !data.video_queue || !data.h264_encode || !data.h264_parse || !data.mpegts_mux || !data.video_convert || !data.hls_sink || !data.app_queue || !data.app_sink) {
//    g_printerr ("Not all elements could be created.\n");
//    return -1;
//  }

  /* Configure wavescope */
//  g_object_set (data.visual, "shader", 0, "style", 0, NULL);

  /* Configure appsrc */
//  gst_audio_info_set_format (&info, GST_AUDIO_FORMAT_S16, SAMPLE_RATE, 1, NULL);
//  audio_caps = gst_audio_info_to_caps (&info);
//  g_object_set (data.app_source, "caps", audio_caps, "format", GST_FORMAT_TIME, NULL);
//  g_signal_connect (data.app_source, "need-data", G_CALLBACK (start_feed), &data);
//  g_signal_connect (data.app_source, "enough-data", G_CALLBACK (stop_feed), &data);
  
  GST_LOG("test pipeline created");
  
  /* Configure appsink */
//  g_object_set (data.app_sink, "emit-signals", TRUE, "caps", audio_caps, NULL);
  g_object_set (data.app_sink, "emit-signals", TRUE, NULL);
  g_signal_connect (data.app_sink, "new-sample", G_CALLBACK (new_sample), &data);
//  gst_caps_unref (audio_caps);

  /* Link all elements that can be automatically linked because they have "Always" pads */
  gst_bin_add_many (GST_BIN (data.pipeline), data.v4l2_source, data.filter, data.tee, data.video_queue, data.video_convert, data.h264_encode, data.h264_parse, data.mpegts_mux, data.hls_sink, data.image_queue, data.multifile_sink, data.app_queue,
      data.app_sink, NULL);
  if (gst_element_link_many (data.v4l2_source, data.tee, NULL) != TRUE ||
      gst_element_link_many (data.video_queue, data.video_convert, data.h264_encode, data.h264_parse, data.mpegts_mux, data.hls_sink, NULL) != TRUE ||
      gst_element_link_many (data.image_queue, data.multifile_sink, NULL) != TRUE ||
      gst_element_link_many (data.app_queue, data.app_sink, NULL) != TRUE) {
    g_printerr ("Elements could not be linked.\n");
    gst_object_unref (data.pipeline);
    return -1;
  }

  /* Manually link the Tee, which has "Request" pads */
//  tee_audio_pad = gst_element_get_request_pad (data.tee, "src_%u");
//  g_print ("Obtained request pad %s for audio branch.\n", gst_pad_get_name (tee_audio_pad));
//  queue_audio_pad = gst_element_get_static_pad (data.audio_queue, "sink");
  tee_video_pad = gst_element_get_request_pad (data.tee, "src_%u");
  g_print ("Obtained request pad %s for video branch.\n", gst_pad_get_name (tee_video_pad));
  queue_video_pad = gst_element_get_static_pad (data.video_queue, "sink");
  tee_image_pad = gst_element_get_request_pad (data.tee, "src_%u");
  g_print ("Obtained request pad %s for image branch.\n", gst_pad_get_name (tee_image_pad));
  queue_image_pad = gst_element_get_static_pad (data.image_queue, "sink");
  tee_app_pad = gst_element_get_request_pad (data.tee, "src_%u");
  g_print ("Obtained request pad %s for app branch.\n", gst_pad_get_name (tee_app_pad));
  queue_app_pad = gst_element_get_static_pad (data.app_queue, "sink");
  if (gst_pad_link (tee_video_pad, queue_video_pad) != GST_PAD_LINK_OK ||
      gst_pad_link (tee_image_pad, queue_image_pad) != GST_PAD_LINK_OK ||
      gst_pad_link (tee_app_pad, queue_app_pad) != GST_PAD_LINK_OK) {
    g_printerr ("Tee could not be linked\n");
    gst_object_unref (data.pipeline);
    return -1;
  }
//  gst_object_unref (queue_audio_pad);
  gst_object_unref (queue_video_pad);
  gst_object_unref (queue_image_pad);
  gst_object_unref (queue_app_pad);

  /* Instruct the bus to emit signals for each received message, and connect to the interesting signals */
  bus = gst_element_get_bus (data.pipeline);
  gst_bus_add_signal_watch (bus);
  g_signal_connect (G_OBJECT (bus), "message::error", (GCallback)error_cb, &data);
  gst_object_unref (bus);

  /* Start playing the pipeline */
  gst_element_set_state (data.pipeline, GST_STATE_PLAYING);

  /* Create a GLib Main Loop and set it to run */
  data.main_loop = g_main_loop_new (NULL, FALSE);
  g_main_loop_run (data.main_loop);

  /* Release the request pads from the Tee, and unref them */
//  gst_element_release_request_pad (data.tee, tee_audio_pad);
  gst_element_release_request_pad (data.tee, tee_video_pad);
  gst_element_release_request_pad (data.tee, tee_image_pad);
  gst_element_release_request_pad (data.tee, tee_app_pad);
//  gst_object_unref (tee_audio_pad);
  gst_object_unref (tee_video_pad);
  gst_object_unref (tee_image_pad);
  gst_object_unref (tee_app_pad);

  /* Free resources */
  gst_element_set_state (data.pipeline, GST_STATE_NULL);
  gst_object_unref (data.pipeline);
  return 0;
}
