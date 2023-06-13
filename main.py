import os
from util import *
import time
import template

class Draft:

    drafts_folder = "D:/JianyingPro Drafts"
    template_folder = "./template/"
    content_file = "draft_content.json"
    meta_info_file = "draft_meta_info.json"

    def __init__(self, name:str="Test"):
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
        self.meta_info['draft_timeline_materials_size_'] = 0
        self.meta_info['tm_draft_create'] = time.time()
        self.meta_info['tm_draft_modified'] = time.time()
        self.meta_info['draft_root_path'] = self.drafts_folder.replace("/","\\\\")
        self.meta_info['draft_removable_storage_device'] = self.drafts_folder.split(':/')[0]

        self.draft_materials:list = self.meta_info['draft_materials'][0]['value']
        self.tracks = DraftTracks(self.content['tracks'])

    def resize(self,width,height):
        """
            修改草稿大小
        """
        self.content['canvas_config']['width'] = width
        self.content['canvas_config']['ratio'] ='custom'
        self.content['canvas_config']['height'] = height

    def save(self):
        """
            保存草稿
        """
        write_json(self.content_path,self.content)
        write_json(self.meta_info_path,self.meta_info)

    def add_media_to_material(self,file_path):
        mate = DraftMaterial(file_path).data
        self.draft_materials.append(mate)
        return mate

    def add_media_to_track(self,file_path,track_index=0):
        mate = self.add_media_to_material(file_path)
        metetype = mate['metetype']
        if metetype == "video" or metetype == "photo":
            self.tracks.add_video_track(track_index)
        elif metetype == "music":
            self.tracks.add_audio_track(track_index)


class DraftMaterial:

    media_type_mapping = {
        "Video": "video",
        "Audio": "music"
    }

    def __init__(self,file_path=None) -> None:
        self.data = None
        if file_path:
            self.file_to_material(file_path)
        
    def file_to_material(self,file_path):
        """
            通过文件的方式去加载为素材
        """
        self.data = template.material()
        media_info = MediaInfo.parse(file_path).to_data()["tracks"][1]
        self.data['metetype'] = self.media_type_mapping[media_info['track_type']]
        if  "width" in media_info:
            self.data["width"] = media_info['width']
            self.data["height"] = media_info['height']
        self.data['duration'] = media_info['duration']
        self.data['extra_info'] = file_path.split("/")[0]
        self.data['file_Path'] = file_path
        return self.data

    def draft_load_material(self):
        """
            从草稿中加载素材
        """
        pass

    def video_material(self,mate):
        canvase = template.canvase()
        speed = template.speed()
        sound_channel_mapping = template.sound_channel_mapping()
        video = template.video()
        video["duration"]= mate['duration'],
        video["height"]= mate['height'],
        video["id"]= generate_id(),
        video["local_material_id"]=mate['id'],
        video["material_name"]= mate['extra_info'],
        video["path"]= mate['file_Path'],
        video["type"]= mate['metetype'],
        video["width"]= mate['width']

class DraftTracks:

    def __init__(self,content=None) -> None:
        self.video_track = []
        self.audio_track = []
        self.text_track = []


    def add_video_track(self,track_index=0):
        track = self.add_track(self.video_track,'video',track_index)
        if track:
            self.video_track.append(track)



    def add_audio_track(self,track_index=0):
        track = self.add_track(self.audio_track,'audio',track_index)
        if track:
            self.audio_track.append(track)


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

if __name__ == "__main__":
    draft = Draft("测试草稿")





