import streamlit as st
import json
import os
import uuid

# 数据存储目录
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 创建角色属性子目录
CHARACTER_ATTR_DIR = os.path.join(DATA_DIR, "character")
if not os.path.exists(CHARACTER_ATTR_DIR):
    os.makedirs(CHARACTER_ATTR_DIR)

# 各 JSON 文件路径
QUALITY_PRESETS_PATH = os.path.join(DATA_DIR, "quality_presets.json")
STYLE_PRESETS_PATH = os.path.join(DATA_DIR, "style_presets.json")
CAMERA_PRESETS_PATH = os.path.join(DATA_DIR, "camera_presets.json")
SCENE_PRESETS_PATH = os.path.join(DATA_DIR, "scene_presets.json")
LIGHTING_PRESETS_PATH = os.path.join(DATA_DIR, "lighting_presets.json")
CHARACTER_PRESETS_PATH = os.path.join(DATA_DIR, "character_presets.json")
PROMPT_COMBINATIONS_PATH = os.path.join(DATA_DIR, "prompt_combinations.json")

# 角色属性文件路径
HAIR_COLOR_PATH = os.path.join(CHARACTER_ATTR_DIR, "hair_color.json")
DEMEANOR_PATH = os.path.join(CHARACTER_ATTR_DIR, "demeanor.json")
EXPRESSION_PATH = os.path.join(CHARACTER_ATTR_DIR, "expression.json")
UNDERWEAR_PATH = os.path.join(CHARACTER_ATTR_DIR, "underwear.json")
OUTFIT_PATH = os.path.join(CHARACTER_ATTR_DIR, "outfit.json")
BODY_TYPE_PATH = os.path.join(CHARACTER_ATTR_DIR, "body_type.json")
POSE_PATH = os.path.join(CHARACTER_ATTR_DIR, "pose.json")
POSTURE_PATH = os.path.join(CHARACTER_ATTR_DIR, "posture.json")

# 如果文件不存在则写入默认内容
def load_json(path, default_data):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=2, ensure_ascii=False)
        return default_data

# --------------------------
# 默认预设内容（参考个人用法典及示例扩充）
default_quality_presets = [
  {
    "name": "High Quality",
    "content": "very awa, masterpiece, best quality, year 2024, newest, highres, absurdres",
    "mode": "replace",
    "remark": "常用高质量标签，例子1/3/4/5均出现"
  }
]

default_style_presets = [
  {
    "name": "Ciloranko Style",
    "content": "ciloranko, (tianliang duohe fangdongye:0.9), ask \\(askzy\\), (wlop:0.8)",
    "mode": "replace",
    "remark": "例子1、4、5中常用画师组合"
  },
  {
    "name": "Flat Color Style",
    "content": "ciloranko, (tianliang duohe fangdongye:0.9), (mikozin:0.6), flat color",
    "mode": "replace",
    "remark": "例子3中使用"
  },
  {
    "name": "Aesthetic Solo",
    "content": "aesthetic, alone, solo, super aesthetic, intricate details, vanripper, lighting, female focus, perfect eyes, colorful, BREAK",
    "mode": "replace",
    "remark": "例子2中的画风描述"
  }
]

default_camera_presets = [
  {
    "name": "Close Up Portrait",
    "content": "close-up, portrait, looking at viewer, from front angle, elegant composition",
    "mode": "replace",
    "remark": "例子1中镜头描述"
  },
  {
    "name": "Full Body",
    "content": "full body, serene(power pose:1.25)",
    "mode": "replace",
    "remark": "例子4中使用"
  },
  {
    "name": "Full-length Portrait",
    "content": "full-length portrait, angry(chassing pose:1.25)",
    "mode": "replace",
    "remark": "例子5中使用"
  }
]

default_scene_presets = [
  {
    "name": "Beach Scene",
    "content": "tropical island, white sand beach, crystal clear turquoise water, palm trees, volcanic rock formation, luxury resort in background, summer setting",
    "mode": "replace",
    "remark": "例子1中的场景描述"
  },
  {
    "name": "Detailed Background",
    "content": "detailed background",
    "mode": "replace",
    "remark": "例子3中简单背景提示"
  },
  {
    "name": "Urban Night",
    "content": "cityscape, neon lights, rainy night",
    "mode": "replace",
    "remark": "补充预设，用于都市风场景"
  }
]

default_lighting_presets = [
  {
    "name": "Golden Hour",
    "content": "golden hour, sunset colors, ocean breeze, warm natural lighting, coastal atmosphere",
    "mode": "replace",
    "remark": "例子1中的打光描述"
  },
  {
    "name": "Fluorescent",
    "content": "fluorescent lighting, light from left, hdr photography",
    "mode": "replace",
    "remark": "例子3中的打光"
  },
  {
    "name": "Moonlight",
    "content": "moonlight light, light from top-right, ektachrome",
    "mode": "replace",
    "remark": "例子4中的打光"
  },
  {
    "name": "Neon Lights",
    "content": "neon lights light, light from top, agfa vista",
    "mode": "replace",
    "remark": "例子5中的打光"
  }
]

# 人物属性默认预设
default_hair_color_presets = [
  {
    "name": "Pink Hair",
    "content": "pink hair",
    "mode": "replace",
    "remark": "粉色头发，常见于角色设定"
  },
  {
    "name": "Blonde Hair",
    "content": "blonde hair, golden locks",
    "mode": "replace",
    "remark": "金发"
  },
  {
    "name": "Black Hair",
    "content": "black hair, raven hair",
    "mode": "replace",
    "remark": "黑发"
  }
]

default_demeanor_presets = [
  {
    "name": "Confident",
    "content": "confident demeanor, self-assured",
    "mode": "replace",
    "remark": "自信的神态"
  },
  {
    "name": "Shy",
    "content": "shy demeanor, timid, bashful",
    "mode": "replace",
    "remark": "害羞的神态"
  },
  {
    "name": "Mysterious",
    "content": "mysterious demeanor, enigmatic",
    "mode": "replace",
    "remark": "神秘的神态"
  }
]

default_expression_presets = [
  {
    "name": "Smile",
    "content": "smiling, happy expression",
    "mode": "replace",
    "remark": "微笑表情"
  },
  {
    "name": "Serious",
    "content": "serious expression, determined face",
    "mode": "replace",
    "remark": "严肃表情"
  },
  {
    "name": "Blushing",
    "content": "blushing, red face, embarrassed expression",
    "mode": "replace", 
    "remark": "脸红表情"
  }
]

default_underwear_presets = [
  {
    "name": "Lace Lingerie",
    "content": "lace lingerie, delicate underwear",
    "mode": "replace",
    "remark": "蕾丝内衣"
  },
  {
    "name": "Silk Bralette",
    "content": "silk bralette, luxury underwear",
    "mode": "replace",
    "remark": "丝绸胸衣"
  },
  {
    "name": "Fishnet",
    "content": "fishnet underwear, revealing lingerie",
    "mode": "replace",
    "remark": "网状内衣"
  }
]

default_outfit_presets = [
  {
    "name": "Business Formal",
    "content": "business formal dress, professional attire",
    "mode": "replace",
    "remark": "商务正装"
  },
  {
    "name": "Gothic Dress",
    "content": "gothic dress, dark elegant outfit",
    "mode": "replace",
    "remark": "哥特风裙装"
  },
  {
    "name": "Casual",
    "content": "casual wear, t-shirt, jeans",
    "mode": "replace",
    "remark": "休闲装"
  }
]

default_body_type_presets = [
  {
    "name": "Slender",
    "content": "slender body, slim figure",
    "mode": "replace",
    "remark": "苗条体型"
  },
  {
    "name": "Athletic",
    "content": "athletic build, toned body, muscular",
    "mode": "replace",
    "remark": "运动型体型"
  },
  {
    "name": "Curvy",
    "content": "curvy figure, hourglass shape",
    "mode": "replace",
    "remark": "丰满体型"
  }
]

default_pose_presets = [
  {
    "name": "Standing",
    "content": "standing, upright position",
    "mode": "replace",
    "remark": "站立动作"
  },
  {
    "name": "Walking",
    "content": "walking, mid-stride",
    "mode": "replace",
    "remark": "行走动作"
  },
  {
    "name": "Running",
    "content": "running, in motion",
    "mode": "replace",
    "remark": "奔跑动作"
  }
]

default_posture_presets = [
  {
    "name": "Power Pose",
    "content": "power pose, hands on hips",
    "mode": "replace",
    "remark": "力量姿势"
  },
  {
    "name": "Elegant",
    "content": "elegant posture, graceful stance",
    "mode": "replace",
    "remark": "优雅姿势"
  },
  {
    "name": "Relaxed",
    "content": "relaxed posture, casual stance",
    "mode": "replace",
    "remark": "放松姿势"
  }
]

default_character_presets = [
  {
    "name": "Chihaya Anon",
    "content": {
      "name": "chihaya anon",
      "series": "genshin impact",
      "hair_color": "pink hair",
      "demeanor": "confident demeanor",
      "expression": "serene expression",
      "underwear": "",
      "outfit": "traditional outfit, elegant dress",
      "body_type": "slender body",
      "pose": "standing",
      "posture": "elegant posture",
      "item": "",
      "extra": "grey eyes"
    },
    "remark": "例子2、5中的角色，触发词格式：角色名 + 系列"
  },
  {
    "name": "Yuigahama Yui",
    "content": {
      "name": "yuigahama yui",
      "series": "",
      "hair_color": "pink hair",
      "demeanor": "cheerful demeanor",
      "expression": "bright smile",
      "underwear": "",
      "outfit": "school uniform",
      "body_type": "slender body",
      "pose": "standing",
      "posture": "power pose",
      "item": "",
      "extra": "red eyes"
    },
    "remark": "例子4中的角色描述"
  }
]

default_prompt_combinations = [
  {
    "name": "Combination Example 1",
    "fields": {
      "quality": {
         "content": "very awa, masterpiece, best quality, year 2024, newest, highres, absurdres",
         "mode": "replace"
      },
      "artists": {
         "content": "ciloranko, (tianliang duohe fangdongye:0.9), ask \\(askzy\\), (wlop:0.8)",
         "mode": "replace"
      },
      "camera": {
         "content": "full-length portrait, angry(chassing pose:1.25)",
         "mode": "replace"
      },
      "scene": {
         "content": "(business formal dress:1.25), (fishnet strappy teddy lingerie:1.25)",
         "mode": "replace"
      },
      "lighting": {
         "content": "neon lights light, light from top, agfa vista",
         "mode": "replace"
      },
      "characters": {
         "content": [
             {
               "name": "chihaya anon",
               "series": "",
               "hair_color": "pink hair",
               "demeanor": "confident demeanor",
               "expression": "serious expression",
               "underwear": "fishnet underwear",
               "outfit": "business formal dress",
               "body_type": "slender body",
               "pose": "standing",
               "posture": "power pose",
               "item": "",
               "extra": "grey eyes, unaligned breasts"
             }
         ],
         "mode": "replace"
      }
    },
    "remark": "例子5：人物、打光、服饰组合预设"
  },
  {
    "name": "Combination Example 2",
    "fields": {
      "quality": {
         "content": "very awa, masterpiece, best quality, year 2024, newest, highres, absurdres",
         "mode": "replace"
      },
      "artists": {
         "content": "ciloranko, (tianliang duohe fangdongye:0.9), ask \\(askzy\\), (wlop:0.8)",
         "mode": "replace"
      },
      "camera": {
         "content": "full body, serene(power pose:1.25)",
         "mode": "replace"
      },
      "scene": {
         "content": "gothic dress:1.25, embroidered silk bralette lingerie:1.25",
         "mode": "replace"
      },
      "lighting": {
         "content": "moonlight light, light from top-right, ektachrome",
         "mode": "replace"
      },
      "characters": {
         "content": [
             {
               "name": "yuigahama yui",
               "series": "",
               "hair_color": "pink hair",
               "demeanor": "cheerful demeanor",
               "expression": "bright smile",
               "underwear": "silk bralette",
               "outfit": "gothic dress",
               "body_type": "slender body",
               "pose": "standing",
               "posture": "elegant posture",
               "item": "",
               "extra": "red eyes"
             }
         ],
         "mode": "replace"
      }
    },
    "remark": "例子4：单角色组合预设"
  }
]

# 读取各预设文件
quality_presets = load_json(QUALITY_PRESETS_PATH, default_quality_presets)
style_presets = load_json(STYLE_PRESETS_PATH, default_style_presets)
camera_presets = load_json(CAMERA_PRESETS_PATH, default_camera_presets)
scene_presets = load_json(SCENE_PRESETS_PATH, default_scene_presets)
lighting_presets = load_json(LIGHTING_PRESETS_PATH, default_lighting_presets)
character_presets = load_json(CHARACTER_PRESETS_PATH, default_character_presets)
prompt_combinations = load_json(PROMPT_COMBINATIONS_PATH, default_prompt_combinations)

# 读取角色属性预设文件
hair_color_presets = load_json(HAIR_COLOR_PATH, default_hair_color_presets)
demeanor_presets = load_json(DEMEANOR_PATH, default_demeanor_presets)
expression_presets = load_json(EXPRESSION_PATH, default_expression_presets)
underwear_presets = load_json(UNDERWEAR_PATH, default_underwear_presets)
outfit_presets = load_json(OUTFIT_PATH, default_outfit_presets)
body_type_presets = load_json(BODY_TYPE_PATH, default_body_type_presets)
pose_presets = load_json(POSE_PATH, default_pose_presets)
posture_presets = load_json(POSTURE_PATH, default_posture_presets)

# 保存 JSON 文件
def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# 预设加载回调函数
def on_preset_change(preset_type, preset_select_key, input_key, mode_key):
    # 当预设选择发生变化时自动应用
    if st.session_state[preset_select_key]:
        presets_map = {
            "quality": quality_presets,
            "style": style_presets,
            "camera": camera_presets,
            "scene": scene_presets,
            "lighting": lighting_presets
        }
        presets = presets_map.get(preset_type, [])
        preset = next((p for p in presets if p["name"] == st.session_state[preset_select_key]), None)
        if preset:
            if st.session_state[mode_key] == "替换":
                st.session_state[input_key] = preset["content"]
            else:
                current = st.session_state[input_key]
                if current and not current.endswith(", "):
                    current += ", "
                st.session_state[input_key] = current + preset["content"]

# 角色属性预设加载回调函数
def on_char_attr_preset_change(preset_type, preset_select_key, input_key, mode_key, char_id):
    if st.session_state[preset_select_key]:
        presets_map = {
            "hair_color": hair_color_presets,
            "demeanor": demeanor_presets,
            "expression": expression_presets,
            "underwear": underwear_presets,
            "outfit": outfit_presets,
            "body_type": body_type_presets,
            "pose": pose_presets,
            "posture": posture_presets
        }
        presets = presets_map.get(preset_type, [])
        preset = next((p for p in presets if p["name"] == st.session_state[preset_select_key]), None)
        if preset:
            full_input_key = f"{input_key}_{char_id}"
            if st.session_state[mode_key] == "替换":
                st.session_state[full_input_key] = preset["content"]
            else:
                current = st.session_state[full_input_key]
                if current and not current.endswith(", "):
                    current += ", "
                st.session_state[full_input_key] = current + preset["content"]

# 拼接提示词函数
def assemble_prompt(quality, style, camera, scene, lighting, characters):
    prompt_parts = []
    if quality.strip():
        prompt_parts.append(quality.strip() + '\n\n')
    if style.strip():
        prompt_parts.append(style.strip() + '\n\n')
    if camera.strip():
        prompt_parts.append(camera.strip() + '\n\n')
    if scene.strip():
        prompt_parts.append(scene.strip() + '\n\n')
    if lighting.strip():
        prompt_parts.append(lighting.strip() + '\n\n')
    # 处理人物部分：多个角色的提示词用逗号隔开
    char_prompts = []
    for char in characters:
        name = char.get("name", "").strip()
        series = char.get("series", "").strip()
        hair_color = char.get("hair_color", "").strip()
        demeanor = char.get("demeanor", "").strip()
        expression = char.get("expression", "").strip()
        underwear = char.get("underwear", "").strip()
        outfit = char.get("outfit", "").strip()
        body_type = char.get("body_type", "").strip()
        pose = char.get("pose", "").strip()
        posture = char.get("posture", "").strip()
        item = char.get("item", "").strip()
        extra = char.get("extra", "").strip()
        
        char_tags = []
        if name:
            if series:
                # 格式：name \(series\), series
                char_tags.append(f"{name} \\({series}\\)")
                char_tags.append(series)
            else:
                char_tags.append(name)
        if hair_color:
            char_tags.append(hair_color)
        if demeanor:
            char_tags.append(demeanor)
        if expression:
            char_tags.append(expression)
        if body_type:
            char_tags.append(body_type)
        if pose:
            char_tags.append(pose)
        if posture:
            char_tags.append(posture)
        if underwear:
            char_tags.append(underwear)
        if outfit:
            char_tags.append(outfit)
        if item:
            char_tags.append(item)
        if extra:
            char_tags.append(extra)
        if char_tags:
            char_prompts.append(", ".join(char_tags))
    if char_prompts:
        prompt_parts.append(", ".join(char_prompts))
    final_prompt = ", ".join(prompt_parts)
    final_prompt = final_prompt.replace(",,", ",")
    return final_prompt

# 初始化各模块的默认值
default_quality = quality_presets[0]["content"] if quality_presets else ""
default_style = style_presets[0]["content"] if style_presets else ""
default_camera = camera_presets[0]["content"] if camera_presets else ""
default_scene = scene_presets[0]["content"] if scene_presets else ""
default_lighting = lighting_presets[0]["content"] if lighting_presets else ""

# 设置 Streamlit 页面
st.set_page_config(page_title="Prompt 生成系统", layout="wide")
page = st.sidebar.selectbox("选择页面", ["生成提示词", "预设管理"])

if page == "生成提示词":
    st.title("Prompt 生成系统")
    st.markdown("按照六大模块输入各部分提示词，并可调用预设。点击下方按钮生成完整的提示词。")
    
    # 模块1：质量词
    st.subheader("1. 质量词")
    col1, col2 = st.columns([3, 1])
    with col1:
        quality_input = st.text_input("请输入质量词（英文逗号分隔）", value=default_quality, key="quality_input")
    with col2:
        preset_names = [p["name"] for p in quality_presets]
        mode_quality = st.radio("应用模式", ["替换", "追加"], index=0, key="quality_mode")
        selected_quality_preset = st.selectbox(
            "选择质量预设", 
            [""] + preset_names, 
            key="quality_preset",
            on_change=on_preset_change,
            args=("quality", "quality_preset", "quality_input", "quality_mode")
        )
    
    # 模块2：画师 + 风格标签
    st.subheader("2. 画师 + 风格标签")
    col1, col2 = st.columns([3, 1])
    with col1:
        style_input = st.text_input("请输入画师/风格标签", value=default_style, key="style_input")
    with col2:
        preset_names = [p["name"] for p in style_presets]
        mode_style = st.radio("应用模式", ["替换", "追加"], index=0, key="style_mode")
        selected_style_preset = st.selectbox(
            "选择画师预设", 
            [""] + preset_names, 
            key="style_preset",
            on_change=on_preset_change,
            args=("style", "style_preset", "style_input", "style_mode")
        )
    
    # 模块3：镜头设置
    st.subheader("3. 镜头设置")
    col1, col2 = st.columns([3, 1])
    with col1:
        camera_input = st.text_input("请输入镜头设置描述", value=default_camera, key="camera_input")
    with col2:
        preset_names = [p["name"] for p in camera_presets]
        mode_camera = st.radio("应用模式", ["替换", "追加"], index=0, key="camera_mode")
        selected_camera_preset = st.selectbox(
            "选择镜头预设", 
            [""] + preset_names, 
            key="camera_preset",
            on_change=on_preset_change,
            args=("camera", "camera_preset", "camera_input", "camera_mode")
        )

    # 模块4：场景设置
    st.subheader("4. 场景设置")
    col1, col2 = st.columns([3, 1])
    with col1:
        scene_input = st.text_input("请输入场景描述", value=default_scene, key="scene_input")
    with col2:
        preset_names = [p["name"] for p in scene_presets]
        mode_scene = st.radio("应用模式", ["替换", "追加"], index=0, key="scene_mode")
        selected_scene_preset = st.selectbox(
            "选择场景预设", 
            [""] + preset_names, 
            key="scene_preset",
            on_change=on_preset_change,
            args=("scene", "scene_preset", "scene_input", "scene_mode")
        )
    
    # 模块5：打光设置
    st.subheader("5. 打光设置")
    col1, col2 = st.columns([3, 1])
    with col1:
        lighting_input = st.text_input("请输入打光描述", value=default_lighting, key="lighting_input")
    with col2:
        preset_names = [p["name"] for p in lighting_presets]
        mode_lighting = st.radio("应用模式", ["替换", "追加"], index=0, key="lighting_mode")
        selected_lighting_preset = st.selectbox(
            "选择打光预设", 
            [""] + preset_names, 
            key="lighting_preset",
            on_change=on_preset_change,
            args=("lighting", "lighting_preset", "lighting_input", "lighting_mode")
        )
    
    # 添加角色预设加载函数
    def load_character_preset(char_id, preset_name):
        preset = next((p for p in character_presets if p["name"] == preset_name), None)
        if preset and preset_name:
            content = preset.get("content", {})
            st.session_state[f"name_{char_id}"] = content.get("name", "")
            st.session_state[f"series_{char_id}"] = content.get("series", "")
            st.session_state[f"hair_color_{char_id}"] = content.get("hair_color", "")
            st.session_state[f"demeanor_{char_id}"] = content.get("demeanor", "")
            st.session_state[f"expression_{char_id}"] = content.get("expression", "")
            st.session_state[f"underwear_{char_id}"] = content.get("underwear", "")
            st.session_state[f"outfit_{char_id}"] = content.get("outfit", "")
            st.session_state[f"body_type_{char_id}"] = content.get("body_type", "")
            st.session_state[f"pose_{char_id}"] = content.get("pose", "")
            st.session_state[f"posture_{char_id}"] = content.get("posture", "")
            st.session_state[f"item_{char_id}"] = content.get("item", "")
            st.session_state[f"extra_{char_id}"] = content.get("extra", "")
            return True
        return False
    
    # 模块6：人物具体设置（动态表单）
    if "character_ids" not in st.session_state:
        st.session_state.character_ids = []
    if st.button("添加角色", key="add_character"):
        st.session_state.character_ids.append(str(uuid.uuid4()))
        st.rerun()
    characters_data = []
    for char_id in st.session_state.character_ids:
        with st.expander(f"角色设置 {char_id}", expanded=True):
            # 添加角色预设选择器
            preset_names = [p["name"] for p in character_presets]
            col1, col2 = st.columns([3, 1])
            with col1:
                selected_char_preset = st.selectbox(
                    "选择角色预设", 
                    [""] + preset_names, 
                    key=f"char_preset_{char_id}"
                )
            with col2:
                if st.button("应用预设", key=f"apply_preset_{char_id}"):
                    if load_character_preset(char_id, selected_char_preset):
                        st.rerun()
            
            # 角色基本信息
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("角色名", key=f"name_{char_id}")
            with col2:
                series = st.text_input("系列", key=f"series_{char_id}")
            
            # 外貌特征部分
            st.markdown("#### 外貌部分")
            
            # 发色
            col1, col2 = st.columns([3, 1])
            with col1:
                hair_color = st.text_input("发色", key=f"hair_color_{char_id}")
            with col2:
                preset_names = [p["name"] for p in hair_color_presets]
                mode_hair = st.radio("应用模式", ["替换", "追加"], index=0, key=f"hair_mode_{char_id}")
                selected_hair_preset = st.selectbox(
                    "选择发色预设", 
                    [""] + preset_names, 
                    key=f"hair_preset_{char_id}",
                    on_change=on_char_attr_preset_change,
                    args=("hair_color", f"hair_preset_{char_id}", "hair_color", f"hair_mode_{char_id}", char_id)
                )
            
            # 神态
            col1, col2 = st.columns([3, 1])
            with col1:
                demeanor = st.text_input("神态", key=f"demeanor_{char_id}")
            with col2:
                preset_names = [p["name"] for p in demeanor_presets]
                mode_demeanor = st.radio("应用模式", ["替换", "追加"], index=0, key=f"demeanor_mode_{char_id}")
                selected_demeanor_preset = st.selectbox(
                    "选择神态预设", 
                    [""] + preset_names, 
                    key=f"demeanor_preset_{char_id}",
                    on_change=on_char_attr_preset_change,
                    args=("demeanor", f"demeanor_preset_{char_id}", "demeanor", f"demeanor_mode_{char_id}", char_id)
                )
            
            # 表情
            col1, col2 = st.columns([3, 1])
            with col1:
                expression = st.text_input("表情", key=f"expression_{char_id}")
            with col2:
                preset_names = [p["name"] for p in expression_presets]
                mode_expression = st.radio("应用模式", ["替换", "追加"], index=0, key=f"expression_mode_{char_id}")
                selected_expression_preset = st.selectbox(
                    "选择表情预设", 
                    [""] + preset_names, 
                    key=f"expression_preset_{char_id}",
                    on_change=on_char_attr_preset_change,
                    args=("expression", f"expression_preset_{char_id}", "expression", f"expression_mode_{char_id}", char_id)
                )
            
            # 体型
            col1, col2 = st.columns([3, 1])
            with col1:
                body_type = st.text_input("体型", key=f"body_type_{char_id}")
            with col2:
                preset_names = [p["name"] for p in body_type_presets]
                mode_body = st.radio("应用模式", ["替换", "追加"], index=0, key=f"body_mode_{char_id}")
                selected_body_preset = st.selectbox(
                    "选择体型预设", 
                    [""] + preset_names, 
                    key=f"body_preset_{char_id}",
                    on_change=on_char_attr_preset_change,
                    args=("body_type", f"body_preset_{char_id}", "body_type", f"body_mode_{char_id}", char_id)
                )
            
            # 服饰部分
            st.markdown("#### 服饰部分")
            
            # 内衣
            col1, col2 = st.columns([3, 1])
            with col1:
                underwear = st.text_input("内衣", key=f"underwear_{char_id}")
            with col2:
                preset_names = [p["name"] for p in underwear_presets]
                mode_underwear = st.radio("应用模式", ["替换", "追加"], index=0, key=f"underwear_mode_{char_id}")
                selected_underwear_preset = st.selectbox(
                    "选择内衣预设", 
                    [""] + preset_names, 
                    key=f"underwear_preset_{char_id}",
                    on_change=on_char_attr_preset_change,
                    args=("underwear", f"underwear_preset_{char_id}", "underwear", f"underwear_mode_{char_id}", char_id)
                )
            
            # 外衣/服装
            col1, col2 = st.columns([3, 1])
            with col1:
                outfit = st.text_input("衣着(外衣)", key=f"outfit_{char_id}")
            with col2:
                preset_names = [p["name"] for p in outfit_presets]
                mode_outfit = st.radio("应用模式", ["替换", "追加"], index=0, key=f"outfit_mode_{char_id}")
                selected_outfit_preset = st.selectbox(
                    "选择服装预设", 
                    [""] + preset_names, 
                    key=f"outfit_preset_{char_id}",
                    on_change=on_char_attr_preset_change,
                    args=("outfit", f"outfit_preset_{char_id}", "outfit", f"outfit_mode_{char_id}", char_id)
                )
            
            # 动作与姿势部分
            st.markdown("#### 动作与姿势")
            
            # 动作
            col1, col2 = st.columns([3, 1])
            with col1:
                pose = st.text_input("动作", key=f"pose_{char_id}")
            with col2:
                preset_names = [p["name"] for p in pose_presets]
                mode_pose = st.radio("应用模式", ["替换", "追加"], index=0, key=f"pose_mode_{char_id}")
                selected_pose_preset = st.selectbox(
                    "选择动作预设", 
                    [""] + preset_names, 
                    key=f"pose_preset_{char_id}",
                    on_change=on_char_attr_preset_change,
                    args=("pose", f"pose_preset_{char_id}", "pose", f"pose_mode_{char_id}", char_id)
                )
            
            # 姿势
            col1, col2 = st.columns([3, 1])
            with col1:
                posture = st.text_input("姿势", key=f"posture_{char_id}")
            with col2:
                preset_names = [p["name"] for p in posture_presets]
                mode_posture = st.radio("应用模式", ["替换", "追加"], index=0, key=f"posture_mode_{char_id}")
                selected_posture_preset = st.selectbox(
                    "选择姿势预设", 
                    [""] + preset_names, 
                    key=f"posture_preset_{char_id}",
                    on_change=on_char_attr_preset_change,
                    args=("posture", f"posture_preset_{char_id}", "posture", f"posture_mode_{char_id}", char_id)
                )
            
            # 其他信息部分
            st.markdown("#### 其他信息")
            item = st.text_input("持有物品", key=f"item_{char_id}")
            extra = st.text_input("额外特征", key=f"extra_{char_id}")
            
            if st.button("删除此角色", key=f"del_{char_id}"):
                st.session_state.character_ids.remove(char_id)
                st.rerun()
            
            characters_data.append({
                "name": name,
                "series": series,
                "hair_color": hair_color,
                "demeanor": demeanor,
                "expression": expression,
                "underwear": underwear,
                "outfit": outfit,
                "body_type": body_type,
                "pose": pose,
                "posture": posture,
                "item": item,
                "extra": extra
            })
    
    st.markdown("---")
    # 组合预设加载部分
    st.subheader("【组合预设加载】")
    preset_comb_names = [pc["name"] for pc in prompt_combinations]
    
    def on_comb_preset_change():
        if st.session_state.comb_preset:
            preset = next((pc for pc in prompt_combinations if pc["name"] == st.session_state.comb_preset), None)
            if preset and "fields" in preset:
                fields = preset["fields"]
                # 对各字段应用预设
                if "quality" in fields:
                    mode = fields["quality"].get("mode", "replace")
                    content = fields["quality"].get("content", "")
                    if mode == "replace":
                        st.session_state.quality_input = content
                    else:
                        st.session_state.quality_input = st.session_state.quality_input + ", " + content
                
                if "artists" in fields:
                    mode = fields["artists"].get("mode", "replace")
                    content = fields["artists"].get("content", "")
                    if mode == "replace":
                        st.session_state.style_input = content
                    else:
                        st.session_state.style_input = st.session_state.style_input + ", " + content
                
                if "camera" in fields:
                    mode = fields["camera"].get("mode", "replace")
                    content = fields["camera"].get("content", "")
                    if mode == "replace":
                        st.session_state.camera_input = content
                    else:
                        st.session_state.camera_input = st.session_state.camera_input + ", " + content
                
                if "scene" in fields:
                    mode = fields["scene"].get("mode", "replace")
                    content = fields["scene"].get("content", "")
                    if mode == "replace":
                        st.session_state.scene_input = content
                    else:
                        st.session_state.scene_input = st.session_state.scene_input + ", " + content
                
                if "lighting" in fields:
                    mode = fields["lighting"].get("mode", "replace")
                    content = fields["lighting"].get("content", "")
                    if mode == "replace":
                        st.session_state.lighting_input = content
                    else:
                        st.session_state.lighting_input = st.session_state.lighting_input + ", " + content
                
                if "characters" in fields:
                    mode = fields["characters"].get("mode", "replace")
                    content = fields["characters"].get("content", [])
                    if mode == "replace":
                        st.session_state.character_ids = []  # 清空已有角色
                        for char in content:
                            new_id = str(uuid.uuid4())
                            st.session_state.character_ids.append(new_id)
                            st.session_state[f"name_{new_id}"] = char.get("name", "")
                            st.session_state[f"series_{new_id}"] = char.get("series", "")
                            st.session_state[f"hair_color_{new_id}"] = char.get("hair_color", "")
                            st.session_state[f"demeanor_{new_id}"] = char.get("demeanor", "")
                            st.session_state[f"expression_{new_id}"] = char.get("expression", "")
                            st.session_state[f"underwear_{new_id}"] = char.get("underwear", "")
                            st.session_state[f"outfit_{new_id}"] = char.get("outfit", "")
                            st.session_state[f"body_type_{new_id}"] = char.get("body_type", "")
                            st.session_state[f"pose_{new_id}"] = char.get("pose", "")
                            st.session_state[f"posture_{new_id}"] = char.get("posture", "")
                            st.session_state[f"item_{new_id}"] = char.get("item", "")
                            st.session_state[f"extra_{new_id}"] = char.get("extra", "")
                    else:
                        for char in content:
                            new_id = str(uuid.uuid4())
                            st.session_state.character_ids.append(new_id)
                            st.session_state[f"name_{new_id}"] = char.get("name", "")
                            st.session_state[f"series_{new_id}"] = char.get("series", "")
                            st.session_state[f"hair_color_{new_id}"] = char.get("hair_color", "")
                            st.session_state[f"demeanor_{new_id}"] = char.get("demeanor", "")
                            st.session_state[f"expression_{new_id}"] = char.get("expression", "")
                            st.session_state[f"underwear_{new_id}"] = char.get("underwear", "")
                            st.session_state[f"outfit_{new_id}"] = char.get("outfit", "")
                            st.session_state[f"body_type_{new_id}"] = char.get("body_type", "")
                            st.session_state[f"pose_{new_id}"] = char.get("pose", "")
                            st.session_state[f"posture_{new_id}"] = char.get("posture", "")
                            st.session_state[f"item_{new_id}"] = char.get("item", "")
                            st.session_state[f"extra_{new_id}"] = char.get("extra", "")
                st.session_state.show_comb_preview = True
                st.experimental_rerun()  # 仍需要刷新页面以更新角色表单

    selected_comb_preset = st.selectbox(
        "选择组合预设", 
        [""] + preset_comb_names, 
        key="comb_preset",
        on_change=on_comb_preset_change
    )
    
    # 显示组合预设预览
    if "show_comb_preview" in st.session_state and st.session_state.show_comb_preview:
        st.success("组合预设加载完毕，请检查各模块输入后再生成提示词")
        st.session_state.show_comb_preview = False
    
    # 生成按钮和结果显示
    if st.button("生成提示词", key="generate_prompt"):
        final_prompt = assemble_prompt(quality_input, style_input, camera_input, scene_input, lighting_input, characters_data)
        st.session_state.final_prompt = final_prompt
        
    # 显示生成的提示词
    if "final_prompt" in st.session_state:
        st.text_area("生成的提示词", st.session_state.final_prompt, height=200)
    else:
        st.info("点击'生成提示词'按钮以查看最终结果")

else:  # 预设管理页面
    st.title("预设管理")
    st.markdown("在此页面，你可以浏览、添加、编辑或删除各模块的预设。")
    tab = st.selectbox("选择管理的预设类型", 
                      ["质量词", "画师 + 风格", "镜头设置", "场景设置", "打光设置", 
                       "发色", "神态", "表情", "内衣", "衣着", "体型", "动作", "姿势", 
                       "人物", "组合预设"])
    
    if tab == "质量词":
        presets = quality_presets
        file_path = QUALITY_PRESETS_PATH
    elif tab == "画师 + 风格":
        presets = style_presets
        file_path = STYLE_PRESETS_PATH
    elif tab == "镜头设置":
        presets = camera_presets
        file_path = CAMERA_PRESETS_PATH
    elif tab == "场景设置":
        presets = scene_presets
        file_path = SCENE_PRESETS_PATH
    elif tab == "打光设置":
        presets = lighting_presets
        file_path = LIGHTING_PRESETS_PATH
    elif tab == "发色":
        presets = hair_color_presets
        file_path = HAIR_COLOR_PATH
    elif tab == "神态":
        presets = demeanor_presets
        file_path = DEMEANOR_PATH
    elif tab == "表情":
        presets = expression_presets
        file_path = EXPRESSION_PATH
    elif tab == "内衣":
        presets = underwear_presets
        file_path = UNDERWEAR_PATH
    elif tab == "衣着":
        presets = outfit_presets
        file_path = OUTFIT_PATH
    elif tab == "体型":
        presets = body_type_presets
        file_path = BODY_TYPE_PATH
    elif tab == "动作":
        presets = pose_presets
        file_path = POSE_PATH
    elif tab == "姿势":
        presets = posture_presets
        file_path = POSTURE_PATH
    elif tab == "人物":
        presets = character_presets
        file_path = CHARACTER_PRESETS_PATH
    elif tab == "组合预设":
        presets = prompt_combinations
        file_path = PROMPT_COMBINATIONS_PATH
    
    st.write("### 预设列表")
    for i, preset in enumerate(presets):
        st.markdown(f"**{i+1}. {preset['name']}**")
        st.markdown(f"内容：{preset.get('content', preset.get('fields', ''))}")
        st.markdown(f"模式：{preset.get('mode', '')}")
        st.markdown(f"备注：{preset.get('remark', '')}")
        if st.button(f"删除预设 {preset['name']}", key=f"del_{tab}_{i}"):
            presets.pop(i)
            save_json(file_path, presets)
            st.success("预设已删除")
            st.rerun()
        st.markdown("---")
    
    st.write("### 添加新的预设")
    new_name = st.text_input("预设名称", key="new_name")
    
    if tab not in ["人物", "组合预设"]:
        new_content = st.text_input("预设内容", key="new_content")
        new_mode = st.selectbox("应用模式", ["替换", "追加"], key="new_mode")
        new_remark = st.text_area("备注", key="new_remark")
        
        if st.button("保存新预设", key="save_new"):
            try:
                new_preset = {"name": new_name, "content": new_content, "mode": new_mode.lower(), "remark": new_remark}
                presets.append(new_preset)
                save_json(file_path, presets)
                st.success("新预设已保存")
                st.rerun()
            except Exception as e:
                st.error(f"保存预设失败：{e}")
                
    elif tab == "人物":
        st.markdown("请输入角色各属性：")
        char_name = st.text_input("角色名", key="new_char_name")
        char_series = st.text_input("系列", key="new_char_series")
        char_hair = st.text_input("发色", key="new_char_hair")
        char_demeanor = st.text_input("神态", key="new_char_demeanor")
        char_expression = st.text_input("表情", key="new_char_expression")
        char_underwear = st.text_input("内衣", key="new_char_underwear")
        char_outfit = st.text_input("衣着(外衣)", key="new_char_outfit")
        char_body = st.text_input("体型", key="new_char_body")
        char_pose = st.text_input("动作", key="new_char_pose")
        char_posture = st.text_input("姿势", key="new_char_posture")
        char_item = st.text_input("持有物品", key="new_char_item")
        char_extra = st.text_input("额外特征", key="new_char_extra")
        new_remark = st.text_area("备注", key="new_remark")
        
        if st.button("保存角色预设", key="save_char"):
            try:
                char_content = {
                    "name": char_name,
                    "series": char_series,
                    "hair_color": char_hair,
                    "demeanor": char_demeanor,
                    "expression": char_expression,
                    "underwear": char_underwear,
                    "outfit": char_outfit,
                    "body_type": char_body,
                    "pose": char_pose,
                    "posture": char_posture,
                    "item": char_item,
                    "extra": char_extra
                }
                new_preset = {"name": new_name, "content": char_content, "remark": new_remark}
                presets.append(new_preset)
                save_json(file_path, presets)
                st.success("新角色预设已保存")
                st.rerun()
            except Exception as e:
                st.error(f"保存角色预设失败：{e}")
    
    else:  # 组合预设
        st.markdown("### 添加组合预设")
        
        # 初始化会话状态以跟踪添加的字段
        if "comb_preset_fields" not in st.session_state:
            st.session_state.comb_preset_fields = {}
        
        if "comb_preset_characters" not in st.session_state:
            st.session_state.comb_preset_characters = []
        
        # 可添加的字段列表
        field_types = {
            "quality": "质量词",
            "artists": "画师 + 风格",
            "camera": "镜头设置",
            "scene": "场景设置",
            "lighting": "打光设置"
        }
        
        # 已添加的非角色字段
        st.subheader("已添加字段")
        for field_key in list(st.session_state.comb_preset_fields.keys()):
            field_data = st.session_state.comb_preset_fields[field_key]
            with st.expander(f"{field_types.get(field_key, field_key)}", expanded=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    field_content = st.text_area(
                        "内容", 
                        value=field_data.get("content", ""),
                        key=f"comb_field_{field_key}_content"
                    )
                with col2:
                    field_mode = st.radio(
                        "模式", 
                        ["replace", "append"], 
                        index=0 if field_data.get("mode", "replace") == "replace" else 1,
                        key=f"comb_field_{field_key}_mode"
                    )
                
                # 更新字段内容
                st.session_state.comb_preset_fields[field_key] = {
                    "content": field_content,
                    "mode": field_mode
                }
                
                if st.button(f"删除{field_types.get(field_key, field_key)}字段", key=f"del_field_{field_key}"):
                    del st.session_state.comb_preset_fields[field_key]
                    st.experimental_rerun()
        
        # 添加非角色字段的下拉框
        available_fields = [field for field in field_types if field not in st.session_state.comb_preset_fields]
        if available_fields:
            col1, col2 = st.columns([3, 1])
            with col1:
                selected_field = st.selectbox("选择要添加的字段", available_fields, format_func=lambda x: field_types.get(x, x))
            with col2:
                if st.button("添加字段", key="add_field") and selected_field:
                    st.session_state.comb_preset_fields[selected_field] = {"content": "", "mode": "replace"}
                    st.experimental_rerun()
        
        # 角色管理
        st.subheader("角色管理")
        for idx, char in enumerate(st.session_state.comb_preset_characters):
            with st.expander(f"角色 {idx+1}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    char_name = st.text_input("角色名", value=char.get("name", ""), key=f"char_{idx}_name")
                with col2:
                    char_series = st.text_input("系列", value=char.get("series", ""), key=f"char_{idx}_series")
                
                char_hair = st.text_input("发色", value=char.get("hair_color", ""), key=f"char_{idx}_hair")
                char_demeanor = st.text_input("神态", value=char.get("demeanor", ""), key=f"char_{idx}_demeanor")
                char_expression = st.text_input("表情", value=char.get("expression", ""), key=f"char_{idx}_expression")
                char_underwear = st.text_input("内衣", value=char.get("underwear", ""), key=f"char_{idx}_underwear")
                char_outfit = st.text_input("衣着(外衣)", value=char.get("outfit", ""), key=f"char_{idx}_outfit")
                char_body = st.text_input("体型", value=char.get("body_type", ""), key=f"char_{idx}_body")
                char_pose = st.text_input("动作", value=char.get("pose", ""), key=f"char_{idx}_pose")
                char_posture = st.text_input("姿势", value=char.get("posture", ""), key=f"char_{idx}_posture")
                char_item = st.text_input("持有物品", value=char.get("item", ""), key=f"char_{idx}_item")
                char_extra = st.text_input("额外特征", value=char.get("extra", ""), key=f"char_{idx}_extra")
                
                # 更新角色数据
                st.session_state.comb_preset_characters[idx] = {
                    "name": char_name,
                    "series": char_series,
                    "hair_color": char_hair,
                    "demeanor": char_demeanor,
                    "expression": char_expression,
                    "underwear": char_underwear,
                    "outfit": char_outfit,
                    "body_type": char_body,
                    "pose": char_pose,
                    "posture": char_posture,
                    "item": char_item,
                    "extra": char_extra
                }
                
                if st.button(f"删除角色 {idx+1}", key=f"del_char_{idx}"):
                    st.session_state.comb_preset_characters.pop(idx)
                    st.experimental_rerun()
        
        # 添加角色按钮
        if st.button("添加角色", key="add_character"):
            st.session_state.comb_preset_characters.append({})
            st.experimental_rerun()
        
        # 显示当前生成的JSON结构
        fields_data = {}
        for field_key, field_data in st.session_state.comb_preset_fields.items():
            fields_data[field_key] = field_data
        
        if st.session_state.comb_preset_characters:
            fields_data["characters"] = {
                "content": st.session_state.comb_preset_characters,
                "mode": "replace"  # 默认为替换模式
            }
        
        # 组合预设名称和备注
        new_name = st.text_input("预设名称", key="comb_new_name")
        new_remark = st.text_area("备注", key="comb_new_remark")
        
        # 预览生成的JSON
        if st.checkbox("预览JSON结构"):
            complete_preset = {
                "name": new_name,
                "fields": fields_data,
                "remark": new_remark
            }
            st.json(complete_preset)
        
        # 保存预设
        if st.button("保存组合预设", key="save_comb"):
            if not new_name:
                st.error("请输入预设名称")
            elif not fields_data:
                st.error("请至少添加一个字段")
            else:
                try:
                    new_preset = {
                        "name": new_name,
                        "fields": fields_data,
                        "remark": new_remark
                    }
                    presets.append(new_preset)
                    save_json(file_path, presets)
                    st.success("新组合预设已保存")
                    
                    # 清空表单
                    st.session_state.comb_preset_fields = {}
                    st.session_state.comb_preset_characters = []
                    st.session_state.comb_new_name = ""
                    st.session_state.comb_new_remark = ""
                    
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"保存组合预设失败：{e}")
        
        # 重置按钮
        if st.button("重置表单"):
            st.session_state.comb_preset_fields = {}
            st.session_state.comb_preset_characters = []
            st.experimental_rerun()
            
    st.info("提示：保存的预设将存入对应的 JSON 文件，下次启动时可自动加载。")
