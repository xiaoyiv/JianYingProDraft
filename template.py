import time
import util

def canvase():
    return {
        "album_image": "",
        "blur": 0.0,
        "color": "",
        "id": util.generate_id(),
        "image": "",
        "image_id": "",
        "image_name": "",
        "source_platform": 0,
        "team_id": "",
        "type": "canvas_color"
    }

def sound_channel_mapping():
    return {
        "audio_channel_mapping": 0,
        "id":  util.generate_id(),
        "is_config_open": False,
        "type": ""
    }

def speed():
    return {
        "curve_speed": None,
        "id": util.generate_id(),
        "mode": 0,
        "speed": 1.0,
        "type": "speed"
    }

def video():
    return {
            "audio_fade": None,
            "cartoon_path": "",
            "category_id": "",
            "category_name": "local",
            "check_flag": 63487,
            "crop": {
            "lower_left_x": 0.0,
            "lower_left_y": 1.0,
            "lower_right_x": 1.0,
            "lower_right_y": 1.0,
            "upper_left_x": 0.0,
            "upper_left_y": 0.0,
            "upper_right_x": 1.0,
            "upper_right_y": 0.0
            },
            "crop_ratio": "free",
            "crop_scale": 1.0,
            "duration": 0,
            "extra_type_option": 0,
            "formula_id": "",
            "freeze": None,
            "gameplay": None,
            "has_audio": True,
            "height": 0,
            "id": "",
            "intensifies_audio_path": "",
            "intensifies_path": "",
            "is_unified_beauty_mode": False,
            "local_id": "",
            "local_material_id":"",
            "material_id": "",
            "material_name": "",
            "material_url": "",
            "matting": {
            "flag": 0,
            "has_use_quick_brush": False,
            "has_use_quick_eraser": False,
            "interactiveTime": [],
            "path": "",
            "strokes": []
            },
            "media_path": "",
            "object_locked": None,
            "path": "",
            "picture_from": "none",
            "picture_set_category_id": "",
            "picture_set_category_name": "",
            "request_id": "",
            "reverse_intensifies_path": "",
            "reverse_path": "",
            "source_platform": 0,
            "stable": None,
            "team_id": "",
            "type":"",
            "video_algorithm": {
            "algorithms": [],
            "deflicker": None,
            "motion_blur_config": None,
            "noise_reduction": None,
            "path": "",
            "time_range": None
            },
            "width": 0
        }

def material():
    return {
        "create_time": int(time.time()),
        "duration": 0,
        "extra_info": "",
        "file_Path": "",
        "height": 0,
        "id": util.generate_id(),
        "import_time": int(time.time()),
        "import_time_ms":  int(time.time())*10^6,
        "md5": "",
        "metetype": "",
        "roughcut_time_range": { "duration": 0, "start": 0 },
        "sub_time_range": { "duration": -1, "start": -1 },
        "type": 0,
        "width": 0
    }

def track():
    return {
      "attribute": 0,
      "flag": 0,
      "id": util.generate_id(),
      "segments":[],
      "type": ""
    }

def segment():
    return {
          "cartoon": False,
          "clip": {
            "alpha": 1.0,
            "flip": { "horizontal": False, "vertical": False },
            "rotation": 0.0,
            "scale": { "x": 1.0, "y": 1.0 },
            "transform": { "x": 0.0, "y": 0.0 }
          },
          "common_keyframes": [],
          "enable_adjust": True,
          "enable_color_curves": True,
          "enable_color_wheels": True,
          "enable_lut": True,
          "enable_smart_color_adjust": False,
          "extra_material_refs": [
          ],
          "group_id": "",
          "hdr_settings": { "intensity": 1.0, "mode": 1, "nits": 1000 },
          "id": util.generate_id(),
          "intensifies_audio": False,
          "is_placeholder": False,
          "is_tone_modify": False,
          "keyframe_refs": [],
          "last_nonzero_volume": 1.0,
          "material_id":"",
          "render_index": 0,
          "reverse": False,
          "source_timerange": { "duration": 0, "start": 0 },
          "speed": 1.0,
          "target_timerange": { "duration": 0, "start": 0 },
          "template_id": "",
          "template_scene": "default",
          "track_attribute": 0,
          "track_render_index": 0,
          "visible": True,
          "volume": 1.0
        }