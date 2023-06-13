import os
from util import *
import time
import template
import librosa

def get_beat(file):
    y, sr = librosa.load(file)
    bpm, beat = librosa.beat.beat_track(y=y, sr=sr)
    beats = list(librosa.frames_to_time(beat, sr=sr))
    beats.pop(0)
    return beats

class Draft:

    drafts_folder = "D:/JianyingPro Drafts"
    template_folder = "./template/"
    content_file = "draft_content.json"
    meta_info_file = "draft_meta_info.json"

    def __init__(self, name:str="Test"):
        # 路径变量
        self.name = name
        self.folder = os.path.join(self.drafts_folder, name)
        self.content_path = os.path.join(self.folder, self.content_file)
        self.meta_info_path = os.path.join(self.folder, self.meta_info_file)
        # 新建项目文件夹
        new_folder(self.folder)
        # 读取草稿模板
        self.content = read_json(os.path.join(self.template_folder,self.content_file))
        self.meta_info = read_json(os.path.join(self.template_folder,self.meta_info_file))
        # 初始化草稿内容信息
        self.content['id'] = generate_id()
        # 初始化素材信息
        self.meta_info['id'] = generate_id()
        self.meta_info['draft_fold_path'] = self.folder.replace("\\",'/')
        self.meta_info['draft_timeline_metetyperials_size_'] = 0
        self.meta_info['tm_draft_create'] = time.time()
        self.meta_info['tm_draft_modified'] = time.time()
        self.meta_info['draft_root_path'] = self.drafts_folder.replace("/","\\\\")
        self.meta_info['draft_removable_storage_device'] = self.drafts_folder.split(':/')[0]
        # 创建变量
        self.draft_materials:list = self.meta_info['draft_materials'][0]['value'] # 草稿素材库
        self.content_materials:list = self.content['materials'] # 内容素材库
        self.tracks = DraftTracks(self.content['tracks']) # 轨道
        self.materials = {}

    def resize(self,width,height):
        """修改草稿大小"""
        self.content['canvas_config']['width'] = width
        self.content['canvas_config']['ratio'] ='custom'
        self.content['canvas_config']['height'] = height

    def save(self):
        """保存草稿"""
        self.content['tracks'] = self.tracks.composite() # 覆盖轨道
        write_json(self.content_path,self.content)
        write_json(self.meta_info_path,self.meta_info)

    def add_media_to_material(self, file_path):
        """添加媒体到素材库"""
        if file_path not in self.materials:
            mate = DraftMaterial(file_path)
            self.materials[file_path] = mate.data
            self.draft_materials.append(mate.data)
            return mate
        else:
            return self.draft_materials.get(file_path)

    def add_media_to_track(self,media,track_index=0):
        """添加媒体到轨道"""
        if type(media) == str:
            # 当media为文件路径时
            if os.path.exists(media):
                mate = self.add_media_to_material(media)
            else:
                print('文本')
        # 直接加载
        elif type(media) == DraftMaterial:
            mate = media
        # 获取素材类型
        metetype = mate.metetype
        # 创建模板
        segment = template.segment()
        # 类型为视频
        if metetype == "video":
            # 加载为内容素材
            video = mate.video_material()
            # 添加轨道
            self.tracks.add_video_track(track_index)
            # 添加到内容素材库
            self.content_materials['canvases'].append(video[0])
            self.content_materials['speeds'].append(video[1])
            self.content_materials['sound_channel_mappings'].append(video[2])
            self.content_materials['videos'].append(video[3])
            # 创建轨道内剪辑片段
            segment['extra_material_refs'] = [video[0]['id'],video[1]['id'],video[2]['id']]
            segment['material_id'] = video[3]['id']
            segment['source_timerange'] = { "duration": video[3]['duration'], "start": 0 }
            segment['target_timerange'] = { "duration": video[3]['duration'], "start": 0 }
        elif metetype == "music":
             # 加载为内容素材
            audio = mate.audio_material()
            # 添加轨道
            self.tracks.add_audio_track(track_index)
            # 添加到内容素材库
            self.content_materials['beats'].append(audio[0])
            self.content_materials['speeds'].append(audio[1])
            self.content_materials['sound_channel_mappings'].append(audio[2])
            self.content_materials['audios'].append(audio[3])
            segment['extra_material_refs'] = [audio[0]['id'],audio[1]['id'],audio[2]['id']]
            segment['material_id'] = audio[3]['id']
            segment['source_timerange'] = { "duration": audio[3]['duration'], "start": 0 }
            segment['target_timerange'] = { "duration": audio[3]['duration'], "start": 0 }

        self.tracks.to_track(metetype,segment,track_index)


class DraftMaterial:

    media_type_mapping = {
        "Video": "video",
        "Audio": "music"
    }

    def __init__(self,file_path=None) -> None:
        self._data = template.material()
        self.metetype = ''
        self.width = 0
        self.height = 0
        self.duration = 0
        self.extra_info = ''
        self.file_Path = ''
        self.id = self._data['id']

        if type(file_path) == str and os.path.exists(file_path):
            self.file_to_material(file_path)
        elif type(file_path) == dict:
            self.draft_load_material(file_path)
        else:
            print('素材加载失败')
        
    @property
    def data(self):
        self._data['metetype'] = self.metetype
        self._data['width'] = self.width
        self._data['height'] = self.height
        self._data['duration'] = self.duration
        self._data['extra_info'] = self.extra_info
        self._data['file_Path'] = self.file_Path
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def file_to_material(self,file_path):
        """
            通过文件的方式去加载为素材
        """
        media_info = MediaInfo.parse(file_path).to_data()["tracks"][1]
        self.metetype = self.media_type_mapping[media_info['track_type']]
        if  "width" in media_info:
            self.width = media_info['width']
            self.height = media_info['height']
        self.duration = media_info['duration']*1000
        self.extra_info= file_path.split("/")[-1]
        self.file_Path = file_path
        return self.data

    def draft_load_material(self,media):
        """
            从草稿中加载素材
        """
        self._data['metetype'] =   media['metetype']
        self._data['width'] =      media['width']
        self._data['height'] =     media['height']
        self._data['duration'] =   media['duration']
        self._data['extra_info'] = media['extra_info']
        self._data['file_Path'] =  media['file_Path']
        return self.data

    def video_material(self):
        """
            return (canvase,speed,sound_channel_mapping,video)
        """
        canvase = template.canvase()
        speed = template.speed()
        sound_channel_mapping = template.sound_channel_mapping()
        video = template.video()
        video["duration"]= self.duration
        video["height"]= self.height
        video["id"]= generate_id()
        video["local_material_id"]= self.id
        video["material_name"]=  self.extra_info
        video["path"]=  self.file_Path
        video["type"]=  self.metetype
        video["width"]=  self.width
        return (canvase,speed,sound_channel_mapping,video)

    def audio_material(self):
        """
            return (beat,speed,sound_channel_mapping,audio)
        """
        speed = template.speed()
        sound_channel_mapping = template.sound_channel_mapping()
        beat = template.beat()
        bt = list(map(lambda x: int(round(x, 3)* 10**6), get_beat(self.file_Path)))
        beat['user_beats'] = bt
        audio = template.audio()
        audio["duration"]= self.duration
        audio["local_material_id"]= self.id        
        audio["name"]=  self.extra_info
        audio["path"]=  self.file_Path
        audio["type"]=  "extract_" + self.metetype
        return (beat,speed,sound_channel_mapping,audio)

class DraftTracks:

    def __init__(self, tracks=[]) -> None:
        self.video_track = [track for track in tracks if track['type'] == 'video']
        self.audio_track = [track for track in tracks if track['type'] == 'audio']
        self.text_track = [track for track in tracks if track['type'] == 'text']

    def add_video_track(self,track_index=0):
        track = self.add_track(self.video_track,'video',track_index)
        if track:
            self.video_track.append(track)

    def add_audio_track(self,track_index=0):
        track = self.add_track(self.audio_track,'audio',track_index)
        if track:
            if len(self.video_track) == 0 :
                self.add_video_track()
            self.audio_track.append(track)

    def add_text_track(self,track_index=0):
        track = self.add_track(self.text_track,'text',track_index)
        if track:
            self.text_track.append(track)

    def add_track(self,tracks,track_type,track_index):
        track_len = len(tracks)
        if track_index == track_len:
            track = template.track()
            track['type'] = track_type
            if track_len:
                track['flag'] = 2
            return track
        else:
            return False

    def to_track(self,metetype,segment,track_index):
        if metetype == "video":
            self.video_track[track_index]['segments'].append(segment)
        elif metetype == "music":
            self.audio_track[track_index]['segments'].append(segment)

    def composite(self):
        """
            将所有轨道合成为一个列表
        """
        track = []
        track.extend(self.video_track)
        track.extend(self.text_track)
        track.extend(self.audio_track)
        return track

if __name__ == "__main__":
    draft = Draft("测试草稿")
    # draft.add_media_to_track('D:/Videos/剪印导出/测试1(1).mp4')
    draft.add_media_to_track("D:/Music/Krubb Wenkroist - Bleach.mp3")
    draft.save()



