# JianYingProDraft

## 说明

1. 实现原理 : `JianYingPro` 项目文件是 `json` 的形式存储的，只需要创建`draft_content.json`,`draft_mate_info.json` 打开软件后会自动补全。
2. 添加一个媒体到轨道顺序 `草稿媒体库` -> `内容媒体库`-> `轨道片段`
3. `add_media_to_track` 会识别媒体类型，加入到对应轨道。
4. 当没有视频轨道时，创建音频轨道会先创建视频轨道。


```python
if __name__ == "__main__":
    # 新建草稿
    draft = Draft("测试草稿") 
    # 将媒体转化为草稿素材
    audio = DraftMaterial("D:/Music/Krubb Wenkroist - Bleach.mp3")
    # 将媒体添加到轨道中
    draft.add_media_to_track(audio)
    draft.add_media_to_track('D:/Videos/剪印导出/测试1(1).mp4')
    # 保存草稿
    draft.save()
```

```python
    drafts_folder = "D:/JianyingPro Drafts"
    template_folder = "./template json/"
    content_file = "draft_content.json"
    meta_info_file = "draft_meta_info.json"
```
