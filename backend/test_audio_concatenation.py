#!/usr/bin/env python3
"""
测试音频拼接功能
"""

import os
import wave
import numpy as np
from app.services.workflow_synthesizer import WorkflowSynthesizer

def create_test_audio_files():
    """创建测试音频文件"""
    test_dir = "test_audio"
    os.makedirs(test_dir, exist_ok=True)
    
    # 创建几个测试音频文件
    sample_rate = 24000
    duration = 1  # 1秒
    
    for i in range(3):
        # 生成不同频率的正弦波作为测试音频
        frequency = 440 + i * 100  # 440Hz, 540Hz, 640Hz
        samples = int(duration * sample_rate)
        t = np.linspace(0, duration, samples, False)
        audio_data = np.sin(2 * np.pi * frequency * t) * 0.3
        audio_data = (audio_data * 32767).astype(np.int16)
        
        # 保存为WAV文件
        filename = os.path.join(test_dir, f"test_audio_{i+1}.wav")
        with wave.open(filename, 'wb') as wavfile:
            wavfile.setnchannels(1)
            wavfile.setsampwidth(2)
            wavfile.setframerate(sample_rate)
            wavfile.writeframes(audio_data.tobytes())
        
        print(f"创建测试音频文件: {filename}")
    
    return [os.path.join(test_dir, f"test_audio_{i+1}.wav") for i in range(3)]

def test_audio_concatenation():
    """测试音频拼接功能"""
    print("开始测试音频拼接功能...")
    
    # 创建测试音频文件
    audio_files = create_test_audio_files()
    
    # 创建合成器实例（仅用于测试拼接功能）
    class MockFlow:
        def __init__(self):
            self.id = "test_flow"
    
    mock_flow = MockFlow()
    synthesizer = WorkflowSynthesizer(mock_flow)
    
    # 测试音频拼接
    output_path = "test_audio/combined.wav"
    try:
        synthesizer._concatenate_audio_files(audio_files, output_path)
        print(f"✅ 音频拼接成功，输出文件: {output_path}")
        
        # 验证输出文件
        if os.path.exists(output_path):
            with wave.open(output_path, 'rb') as wavfile:
                frames = wavfile.getnframes()
                sample_rate = wavfile.getframerate()
                duration = frames / sample_rate
                print(f"✅ 拼接后音频时长: {duration:.2f} 秒")
                print(f"✅ 采样率: {sample_rate} Hz")
                print(f"✅ 声道数: {wavfile.getnchannels()}")
        else:
            print("❌ 输出文件不存在")
            
    except Exception as e:
        print(f"❌ 音频拼接失败: {e}")

def test_zip_creation():
    """测试ZIP创建功能"""
    print("\n开始测试ZIP创建功能...")
    
    # 创建合成器实例
    class MockFlow:
        def __init__(self):
            self.id = "test_flow"
    
    mock_flow = MockFlow()
    synthesizer = WorkflowSynthesizer(mock_flow)
    
    # 测试ZIP创建
    source_dir = "test_audio"
    zip_path = "test_audio/test_flow.zip"
    
    try:
        synthesizer._create_zip_archive(source_dir, zip_path)
        print(f"✅ ZIP创建成功，文件: {zip_path}")
        
        # 验证ZIP文件
        if os.path.exists(zip_path):
            import zipfile
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                file_list = zipf.namelist()
                print(f"✅ ZIP文件包含 {len(file_list)} 个文件:")
                for file in file_list:
                    print(f"   - {file}")
        else:
            print("❌ ZIP文件不存在")
            
    except Exception as e:
        print(f"❌ ZIP创建失败: {e}")

if __name__ == "__main__":
    test_audio_concatenation()
    test_zip_creation()
    print("\n测试完成！") 