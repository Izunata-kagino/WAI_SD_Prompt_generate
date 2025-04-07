import streamlit as st
import json
import os
import uuid
import random  # Add import for random module
import socket
import threading
from flask import Flask, request, jsonify
from preset import *

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
        
        # 不再在这里处理随机选项，而是记录选择了Random
        if st.session_state[preset_select_key] != "Random":
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
        
        # 不再在这里处理随机选项，而是记录选择了Random
        if st.session_state[preset_select_key] != "Random":    
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

# 查找可用端口
def find_available_port(start_port=5000, max_port=5050):
    for port in range(start_port, max_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        if result != 0:  # 端口未被占用
            return port
    return None

# 创建API服务器
def create_api_server(port, app_state):
    api_app = Flask(__name__)
    
    @api_app.route('/generate_prompt', methods=['POST'])
    def api_generate_prompt():
        try:
            data = request.json
            
            # 处理输入数据
            quality = data.get('quality', '')
            style = data.get('style', '')
            camera = data.get('camera', '')
            scene = data.get('scene', '')
            lighting = data.get('lighting', '')
            characters = data.get('characters', [])
            
            # 处理随机预设
            quality, style, camera, scene, lighting, characters = process_random_presets(
                quality, style, camera, scene, lighting, characters)
            
            # 生成提示词
            prompt = assemble_prompt(quality, style, camera, scene, lighting, characters)
            
            return jsonify({
                'status': 'success',
                'prompt': prompt,
                'quality': quality,
                'style': style,
                'camera': camera,
                'scene': scene,
                'lighting': lighting,
                'characters': characters
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    api_app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

# 启动API服务器
def start_api_server(port, app_state):
    api_thread = threading.Thread(
        target=create_api_server, 
        args=(port, app_state),
        daemon=True
    )
    api_thread.start()
    return api_thread

# 处理随机预设
def process_random_presets(quality, style, camera, scene, lighting, characters):
    # 处理主要预设的随机选择
    if quality == "Random" and quality_presets:
        quality = random.choice(quality_presets)["content"]
    
    if style == "Random" and style_presets:
        style = random.choice(style_presets)["content"]
    
    if camera == "Random" and camera_presets:
        camera = random.choice(camera_presets)["content"]
    
    if scene == "Random" and scene_presets:
        scene = random.choice(scene_presets)["content"]
    
    if lighting == "Random" and lighting_presets:
        lighting = random.choice(lighting_presets)["content"]
    
    # 处理角色属性的随机选择
    for char in characters:
        if char.get("hair_color") == "Random" and hair_color_presets:
            char["hair_color"] = random.choice(hair_color_presets)["content"]
        
        if char.get("demeanor") == "Random" and demeanor_presets:
            char["demeanor"] = random.choice(demeanor_presets)["content"]
        
        if char.get("expression") == "Random" and expression_presets:
            char["expression"] = random.choice(expression_presets)["content"]
        
        if char.get("underwear") == "Random" and underwear_presets:
            char["underwear"] = random.choice(underwear_presets)["content"]
        
        if char.get("outfit") == "Random" and outfit_presets:
            char["outfit"] = random.choice(outfit_presets)["content"]
        
        if char.get("body_type") == "Random" and body_type_presets:
            char["body_type"] = random.choice(body_type_presets)["content"]
        
        if char.get("pose") == "Random" and pose_presets:
            char["pose"] = random.choice(pose_presets)["content"]
        
        if char.get("posture") == "Random" and posture_presets:
            char["posture"] = random.choice(posture_presets)["content"]
    
    return quality, style, camera, scene, lighting, characters

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
    # 处理人物部分：多个角色的提示词用括号包围
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
            char_tags.append(hair_color + '\n')
        if demeanor:
            char_tags.append(demeanor + '\n')
        if expression:
            char_tags.append(expression + '\n')
        if body_type:
            char_tags.append(body_type)
        if pose:
            char_tags.append(pose + '\n')
        if posture:
            char_tags.append(posture + '\n')
        if underwear:
            char_tags.append(underwear)
        if outfit:
            char_tags.append(outfit)
        if item:
            char_tags.append(item + '\n')
        if extra:
            char_tags.append(extra)
        if char_tags:
            # 每个角色的描述用括号包围
            char_prompts.append("BREAK,\n(" + ", ".join(char_tags) + ")\n")
    
    # 添加角色数量提示(除了单角色情况)
    if len(char_prompts) > 1:
        prompt_parts.append(f"{len(char_prompts)} girls, \n\n" + ", ".join(char_prompts))
    elif len(char_prompts) == 1:
        prompt_parts.append(char_prompts[0])
    
    final_prompt = ", ".join(prompt_parts)
    final_prompt = final_prompt.replace(",,", ",")
    return final_prompt

# 初始化各模块的默认值
default_quality = quality_presets[0]["content"] if quality_presets else ""
default_style = style_presets[0]["content"] if style_presets else ""
default_camera = camera_presets[0]["content"] if camera_presets else ""
default_scene = scene_presets[0]["content"] if scene_presets else ""
default_lighting = lighting_presets[0]["content"] if lighting_presets else ""

# 初始化API状态
if 'api_running' not in st.session_state:
    st.session_state.api_running = False
    st.session_state.api_port = None
    st.session_state.api_thread = None

# 设置 Streamlit 页面
st.set_page_config(page_title="Prompt 生成系统", layout="wide")
page = st.sidebar.selectbox("选择页面", ["生成提示词", "预设管理", "API设置"])

if page == "生成提示词":
    st.title("Prompt 生成系统")
    st.markdown("按照六大模块输入各部分提示词，并可调用预设。点击下方按钮生成完整的提示词。")
    
    # 模块1：质量词
    st.subheader("1. 质量词")
    col1, col2 = st.columns([3, 1])
    with col1:
        quality_input = st.text_input("请输入质量词（英文逗号分隔）", value=default_quality, key="quality_input")
    with col2:
        preset_names = ["Random"] + [p["name"] for p in quality_presets]
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
        preset_names = ["Random"] + [p["name"] for p in style_presets]
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
        preset_names = ["Random"] + [p["name"] for p in camera_presets]
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
        preset_names = ["Random"] + [p["name"] for p in scene_presets]
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
        preset_names = ["Random"] + [p["name"] for p in lighting_presets]
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
            preset_names = ["Random"] + [p["name"] for p in character_presets]
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
                preset_names = ["Random"] + [p["name"] for p in hair_color_presets]
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
                preset_names = ["Random"] + [p["name"] for p in demeanor_presets]
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
                preset_names = ["Random"] + [p["name"] for p in expression_presets]
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
                preset_names = ["Random"] + [p["name"] for p in body_type_presets]
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
                preset_names = ["Random"] + [p["name"] for p in underwear_presets]
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
                preset_names = ["Random"] + [p["name"] for p in outfit_presets]
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
                preset_names = ["Random"] + [p["name"] for p in pose_presets]
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
                preset_names = ["Random"] + [p["name"] for p in posture_presets]
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
        # 处理所有随机预设
        quality = quality_input
        style = style_input
        camera = camera_input
        scene = scene_input
        lighting = lighting_input
        
        # 在生成提示词时处理随机预设
        if selected_quality_preset == "Random" and quality_presets:
            quality = random.choice(quality_presets)["content"]
            
        if selected_style_preset == "Random" and style_presets:
            style = random.choice(style_presets)["content"]
            
        if selected_camera_preset == "Random" and camera_presets:
            camera = random.choice(camera_presets)["content"]
            
        if selected_scene_preset == "Random" and scene_presets:
            scene = random.choice(scene_presets)["content"]
            
        if selected_lighting_preset == "Random" and lighting_presets:
            lighting = random.choice(lighting_presets)["content"]
        
        # 处理角色属性的随机预设
        for char in characters_data:
            char_id = st.session_state.character_ids[characters_data.index(char)]
            
            if st.session_state.get(f"hair_preset_{char_id}") == "Random" and hair_color_presets:
                char["hair_color"] = random.choice(hair_color_presets)["content"]
                
            if st.session_state.get(f"demeanor_preset_{char_id}") == "Random" and demeanor_presets:
                char["demeanor"] = random.choice(demeanor_presets)["content"]
                
            if st.session_state.get(f"expression_preset_{char_id}") == "Random" and expression_presets:
                char["expression"] = random.choice(expression_presets)["content"]
                
            if st.session_state.get(f"underwear_preset_{char_id}") == "Random" and underwear_presets:
                char["underwear"] = random.choice(underwear_presets)["content"]
                
            if st.session_state.get(f"outfit_preset_{char_id}") == "Random" and outfit_presets:
                char["outfit"] = random.choice(outfit_presets)["content"]
                
            if st.session_state.get(f"body_preset_{char_id}") == "Random" and body_type_presets:
                char["body_type"] = random.choice(body_type_presets)["content"]
                
            if st.session_state.get(f"pose_preset_{char_id}") == "Random" and pose_presets:
                char["pose"] = random.choice(pose_presets)["content"]
                
            if st.session_state.get(f"posture_preset_{char_id}") == "Random" and posture_presets:
                char["posture"] = random.choice(posture_presets)["content"]

        final_prompt = assemble_prompt(quality, style, camera, scene, lighting, characters_data)
        st.session_state.final_prompt = final_prompt
        
    # 显示生成的提示词
    if "final_prompt" in st.session_state:
        st.text_area("生成的提示词", st.session_state.final_prompt, height=200)
    else:
        st.info("点击'生成提示词'按钮以查看最终结果")

elif page == "API设置":
    st.title("API 设置")
    st.markdown("在此页面，你可以开启或关闭API服务，允许其他应用程序通过HTTP请求生成提示词。")
    
    # API 状态显示
    if st.session_state.api_running:
        st.success(f"API服务正在运行于端口：{st.session_state.api_port}")
        st.markdown(f"""
        ### API 使用方法
        
        1. 请求地址: `http://localhost:{st.session_state.api_port}/generate_prompt`
        2. 请求方法: `POST`
        3. 请求格式: `application/json`
        4. 请求体示例:
        ```json
        {{
            "quality": "8k, masterpiece, best quality, ultra-detailed",
            "style": "oil painting, concept art",
            "camera": "wide shot",
            "scene": "forest, autumn",
            "lighting": "golden hour, sunset lighting",
            "characters": [
                {{
                    "name": "Alice",
                    "series": "Wonderland",
                    "hair_color": "blonde",
                    "demeanor": "curious",
                    "expression": "smiling",
                    "underwear": "",
                    "outfit": "blue dress, white apron",
                    "body_type": "slim",
                    "pose": "standing",
                    "posture": "upright",
                    "item": "pocket watch",
                    "extra": ""
                }}
            ]
        }}
        ```
        5. 响应示例:
        ```json
        {{
            "status": "success",
            "prompt": "...", // 生成的完整提示词
            "quality": "...", // 处理后的质量词
            "style": "...", // 处理后的风格词
            "camera": "...", // 处理后的镜头设置
            "scene": "...", // 处理后的场景设置
            "lighting": "...", // 处理后的打光设置
            "characters": [...] // 处理后的角色数据
        }}
        ```
        
        **特别说明**：对于随机功能，可以将任何字段设置为 "Random"，API将自动随机选择预设。
        """)
        
        # 关闭API按钮
        if st.button("关闭API服务"):
            # 仅将状态标记为关闭，线程会自动结束
            st.session_state.api_running = False
            st.session_state.api_port = None
            st.session_state.api_thread = None
            st.success("API服务已关闭")
            st.rerun()
    else:
        st.warning("API服务当前未运行")
        
        # 开启API按钮
        if st.button("启动API服务"):
            # 查找可用端口
            port = find_available_port()
            if port:
                # 启动API服务器
                api_thread = start_api_server(port, st.session_state)
                st.session_state.api_running = True
                st.session_state.api_port = port
                st.session_state.api_thread = api_thread
                st.success(f"API服务已启动于端口：{port}")
                st.rerun()
            else:
                st.error("无法找到可用端口，请检查5000-5050端口范围是否被占用")

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
