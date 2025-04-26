import tkinter as tk
from tkinter import messagebox
import time
import webbrowser

class CPSTester:
    def __init__(self, root):
        self.root = root
        self.language = "zh_cn"
        self.texts = {
            "zh_cn": {
                "title": "CPS测试器",
                "duration": "测试时间(秒):",
                "instruction": "设置时间后点击下方按钮开始测试",
                "count": "点击次数: {0}",
                "cps": "CPS: {0:.1f}",
                "time_left": "剩余时间: {0}",
                "start": "点击开始测试",
                "click": "点击!",
                "complete": "测试完成!",
                "author": "Made By Jerry1145yard",
                "warning": "用连点器的没有真本事",
                "reset": "重置",
                "share": "分享成绩",
                "bilibili": "作者B站主页",
                "github": "作者GitHub",
                "error": "错误",
                "invalid_number": "请输入有效数字",
                "result": "测试完成!\nCPS: {0:.1f}",
                "share_success": "分享成功",
                "share_msg": "成绩已复制到剪贴板\n直接粘贴即可分享！"
            },
            "zh_tw": {
                "title": "CPS測試器",
                "duration": "測試時間(秒):",
                "instruction": "設定時間後點擊下方按鈕開始測試",
                "count": "點擊次數: {0}",
                "cps": "CPS: {0:.1f}",
                "time_left": "剩餘時間: {0}",
                "start": "點擊開始測試",
                "click": "點擊!",
                "complete": "測試完成!",
                "author": "Made By Jerry1145yard",
                "warning": "使用連點器不算真本事",
                "reset": "重置",
                "share": "分享成績",
                "bilibili": "作者B站主頁",
                "github": "作者GitHub",
                "error": "錯誤",
                "invalid_number": "請輸入有效數字",
                "result": "測試完成!\nCPS: {0:.1f}",
                "share_success": "分享成功",
                "share_msg": "成績已複製到剪貼簿\n直接貼上即可分享！"
            },
            "en": {
                "title": "CPS Tester",
                "duration": "Duration(sec):",
                "instruction": "Set time and click button to start",
                "count": "Clicks: {0}",
                "cps": "CPS: {0:.1f}",
                "time_left": "Time left: {0}",
                "start": "Start Test",
                "click": "Click!",
                "complete": "Test Complete!",
                "author": "Made By Jerry1145yard",
                "warning": "Auto-clickers have no real skill",
                "reset": "Reset",
                "share": "Share Result",
                "bilibili": "Bilibili",
                "github": "GitHub",
                "error": "Error",
                "invalid_number": "Please enter a valid number",
                "result": "Test Complete!\nCPS: {0:.1f}",
                "share_success": "Success",
                "share_msg": "Result copied to clipboard!\nPaste to share."
            }
        }
        self.root.title(self.texts[self.language]["title"])
        self.root.geometry("560x580")
        
        # 初始化状态变量
        self.test_started = False
        self.start_time = 0
        self.click_count = 0
        self.test_duration = 10
        self.last_cps = 0.0
        
        # 创建UI组件
        self.create_widgets()
    
    def create_widgets(self):
        # 主框架
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # 语言切换栏
        self.lang_frame = tk.Frame(self.main_frame)
        self.lang_frame.pack(pady=3)
        
        self.zh_cn_button = tk.Button(
            self.lang_frame,
            text="简体",
            command=lambda: self.change_language("zh_cn"),
            font=("Microsoft JhengHei", 9),
            width=4
        )
        self.zh_cn_button.pack(side=tk.LEFT, padx=2)
        
        self.zh_tw_button = tk.Button(
            self.lang_frame,
            text="繁體",
            command=lambda: self.change_language("zh_tw"),
            font=("Microsoft JhengHei", 9),
            width=4
        )
        self.zh_tw_button.pack(side=tk.LEFT, padx=2)
        
        self.en_button = tk.Button(
            self.lang_frame,
            text="English",
            command=lambda: self.change_language("en"),
            font=("Microsoft JhengHei", 9),
            width=5
        )
        self.en_button.pack(side=tk.LEFT, padx=2)
        
        # 标题
        self.title_label = tk.Label(self.main_frame, 
                                  font=("Microsoft JhengHei", 24))
        
        # 时间设置组件
        self.duration_frame = tk.Frame(self.main_frame)
        self.duration_label = tk.Label(self.duration_frame, 
                                     font=("Microsoft JhengHei", 12))
        self.duration_entry = tk.Entry(
            self.duration_frame,
            font=("Microsoft JhengHei", 12),
            width=5,
            validate="key"
        )
        self.duration_entry.insert(0, "10")
        vcmd = (self.root.register(self.validate_duration), '%P')
        self.duration_entry.config(validatecommand=vcmd)
        
        # 其他UI组件
        self.instruction_label = tk.Label(self.main_frame, font=("Microsoft JhengHei", 12))
        self.count_label = tk.Label(self.main_frame, font=("Microsoft JhengHei", 16))
        self.cps_label = tk.Label(self.main_frame, font=("Microsoft JhengHei", 16))
        self.time_label = tk.Label(self.main_frame, font=("Microsoft JhengHei", 14))
        
        # 主按钮
        self.click_button = tk.Button(
            self.main_frame,
            bg="#4CAF50",
            fg="#FFFFFF",
            font=("Microsoft JhengHei", 14),
            height=2,
            width=15
        )
        
        # 信息标签
        self.author_label = tk.Label(self.main_frame, font=("Microsoft JhengHei", 10), fg="#666666")
        self.warning_label = tk.Label(self.main_frame, font=("Microsoft JhengHei", 10, "bold"), fg="#FF0000")
        
        # 底部按钮
        self.bottom_frame = tk.Frame(self.main_frame)
        self.reset_button = tk.Button(
            self.bottom_frame,
            bg="#f44336",
            fg="#FFFFFF",
            font=("Microsoft JhengHei", 12),
            height=1,
            width=6,
            command=self.reset_test
        )
        self.share_button = tk.Button(
            self.bottom_frame,
            bg="#9C27B0",
            fg="#FFFFFF",
            font=("Microsoft JhengHei", 12),
            height=1,
            width=8,
            state=tk.DISABLED,
            command=self.share_result
        )
        self.bilibili_button = tk.Button(
            self.bottom_frame,
            bg="#23ADE5",
            fg="#FFFFFF",
            font=("Microsoft JhengHei", 12),
            height=1,
            width=12,
            command=self.open_bilibili
        )
        self.github_button = tk.Button(
            self.bottom_frame,
            bg="#000000",
            fg="#FFFFFF",
            font=("Microsoft JhengHei", 12),
            height=1,
            width=10,
            command=self.open_github
        )

        # 布局组件
        self.title_label.pack(pady=5)
        self.duration_frame.pack(pady=5)
        self.duration_label.pack(side=tk.LEFT)
        self.duration_entry.pack(side=tk.LEFT, padx=5)
        self.instruction_label.pack(pady=5)
        self.count_label.pack(pady=5)
        self.cps_label.pack(pady=5)
        self.time_label.pack(pady=5)
        self.click_button.pack(pady=10)
        self.author_label.pack()
        self.warning_label.pack()
        self.bottom_frame.pack(side=tk.BOTTOM, pady=10)
        self.reset_button.pack(side=tk.LEFT, padx=2)
        self.share_button.pack(side=tk.LEFT, padx=2)
        self.bilibili_button.pack(side=tk.RIGHT, padx=2)
        self.github_button.pack(side=tk.RIGHT, padx=2)
        
        # 初始化文本
        self.change_language("zh_cn")

    def change_language(self, lang):
        """更新界面语言"""
        self.language = lang
        texts = self.texts[lang]
        
        # 更新所有文本内容
        components = [
            (self.root, "title"),
            (self.title_label, "title"),
            (self.duration_label, "duration"),
            (self.instruction_label, "instruction"),
            (self.count_label, "count"),
            (self.cps_label, "cps"),
            (self.time_label, "time_left"),
            (self.author_label, "author"),
            (self.warning_label, "warning"),
            (self.reset_button, "reset"),
            (self.share_button, "share"),
            (self.bilibili_button, "bilibili"),
            (self.github_button, "github"),
            (self.click_button, "start")
        ]
        
        for component, key in components:
            text = texts[key]
            if key == "count":
                text = text.format(self.click_count)
            elif key == "cps":
                text = text.format(self.last_cps if self.last_cps > 0 else 0.0)
            elif key == "time_left":
                if not self.test_started:
                    remaining = int(self.test_duration)
                else:
                    remaining = max(0, self.test_duration - (time.time() - self.start_time))
                text = text.format(f"{remaining:.1f}" if self.test_started else str(remaining))
            
            if isinstance(component, tk.Tk):
                component.title(text)
            else:
                component.config(text=text)
        
        # 更新开始按钮状态
        if self.test_started:
            self.click_button.config(text=texts["click"], command=self.handle_click)
        else:
            self.click_button.config(text=texts["start"], command=self.start_test)

    def start_test(self):
        """启动新的测试"""
        if self.test_started:
            return
            
        input_text = self.duration_entry.get().strip()
        if not input_text:
            self.test_duration = 10
        else:
            try:
                self.test_duration = max(1, int(input_text))
            except ValueError:
                messagebox.showerror(
                    self.texts[self.language]["error"],
                    self.texts[self.language]["invalid_number"],
                    parent=self.root
                )
                return
            
        self.test_started = True
        self.start_time = time.time()
        self.click_count = 0
        
        # 立即更新按钮功能
        self.click_button.config(
            text=self.texts[self.language]["click"],
            command=self.handle_click
        )
        
        # 更新界面状态
        self.time_label.config(text=self.texts[self.language]["time_left"].format(str(self.test_duration)))
        self.count_label.config(text=self.texts[self.language]["count"].format(0))
        self.duration_entry.config(state=tk.DISABLED)
        self.share_button.config(state=tk.DISABLED)
        
        # 启动计时器
        self.update_timer()

    def handle_click(self):
        """处理点击事件"""
        if self.test_started:
            self.click_count += 1
            new_text = self.texts[self.language]["count"].format(self.click_count)
            self.count_label.config(text=new_text)

    def update_timer(self):
        """更新倒计时"""
        if self.test_started:
            elapsed = time.time() - self.start_time
            remaining = max(0, self.test_duration - elapsed)
            time_text = self.texts[self.language]["time_left"].format(f"{remaining:.1f}")
            self.time_label.config(text=time_text)
            
            if remaining <= 0:
                self.test_complete()
            else:
                self.root.after(100, self.update_timer)

    def test_complete(self):
        """完成测试"""
        self.test_started = False
        self.last_cps = self.click_count / self.test_duration
        
        # 更新结果
        self.cps_label.config(text=self.texts[self.language]["cps"].format(self.last_cps))
        self.click_button.config(
            text=self.texts[self.language]["complete"],
            state=tk.DISABLED
        )
        self.share_button.config(state=tk.NORMAL)
        
        # 显示结果
        messagebox.showinfo(
            self.texts[self.language]["result"].split("!")[0] + "!",
            self.texts[self.language]["result"].format(self.last_cps),
            parent=self.root
        )

    def reset_test(self):
        """重置所有状态"""
        self.test_started = False
        self.click_count = 0
        self.last_cps = 0.0
        
        # 重置界面元素
        self.count_label.config(text=self.texts[self.language]["count"].format(0))
        self.cps_label.config(text=self.texts[self.language]["cps"].format(0.0))
        self.time_label.config(text=self.texts[self.language]["time_left"].format(str(self.test_duration)))
        self.click_button.config(
            text=self.texts[self.language]["start"],
            command=self.start_test,
            state=tk.NORMAL
        )
        self.duration_entry.config(state=tk.NORMAL)
        self.share_button.config(state=tk.DISABLED)
        self.root.update()

    def share_result(self):
        """分享测试结果"""
        share_text = {
            "zh_cn": f"我在CPS测试器中获得了 {self.last_cps:.1f}/S 的CPS！下载：https://github.com/Jerry1145yard/CpsTester/releases",
            "zh_tw": f"我在CPS測試器中獲得了 {self.last_cps:.1f}/S 的CPS！下載：https://github.com/Jerry1145yard/CpsTester/releases",
            "en": f"I got {self.last_cps:.1f} CPS in CPS Tester! Download:https://github.com/Jerry1145yard/CpsTester/releases"
        }[self.language]
        
        self.root.clipboard_clear()
        self.root.clipboard_append(share_text)
        messagebox.showinfo(
            self.texts[self.language]["share_success"],
            self.texts[self.language]["share_msg"],
            parent=self.root
        )

    def validate_duration(self, new_value):
        """验证输入有效性"""
        return new_value.isdigit() or new_value == ""

    def open_bilibili(self):
        webbrowser.open("https://space.bilibili.com/1225634448")

    def open_github(self):
        webbrowser.open("https://github.com/Jerry1145yard")

if __name__ == "__main__":
    root = tk.Tk()
    app = CPSTester(root)
    root.mainloop()
