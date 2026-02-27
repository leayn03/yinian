const { createApp } = Vue;

createApp({
    data() {
        return {
            // 页面状态
            currentPage: 'splash',
            previousPage: '',

            // 用户输入
            userWish: '',

            // 签文数据
            allFortunes: [],
            currentFortune: null,

            // 历史记录
            history: [],

            // 摇动状态
            isShaking: false,
            shakeThreshold: 25,
            lastShakeTime: 0,

            // 设置
            settings: {
                haptic: true,
                sound: true
            },

            // UI 状态
            showMenu: false,
            showImageSide: 'front',  // 'front' 或 'back'
            fullscreenImage: null,   // 全屏显示的图片路径
            toast: {
                show: false,
                message: '',
                type: 'info'
            },

            // 设备检测
            isMobile: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
        };
    },

    computed: {
        // 签级颜色映射（浅草寺签级）
        levelColors() {
            return {
                '大吉': '#D4AF37',    // 金色
                '吉': '#8B9A7A',      // 淡墨绿
                '半吉': '#9BA17B',    // 浅绿
                '小吉': '#A8B69A',    // 更浅的绿
                '末吉': '#B8C5A8',    // 极浅绿
                '凶': '#A0A0A0',      // 灰色
                '大凶': '#8B7D6B'     // 灰褐
            };
        },

        // 解读章节
        interpretationSections() {
            if (!this.currentFortune) return [];
            const interp = this.currentFortune.interpretation;
            const sections = [
                { title: '整体运势', content: interp.summary },
                { title: '事业财运', content: interp.career },
                { title: '感情姻缘', content: interp.love },
                { title: '健康平安', content: interp.health },
                { title: '建议', content: interp.advice }
            ];

            if (interp.story) {
                sections.push({ title: '典故', content: interp.story });
            }

            return sections;
        }
    },

    mounted() {
        console.log('🎨 一念 APP 启动');

        // 加载签文数据
        this.loadFortunes();

        // 加载历史记录
        this.loadHistory();

        // 加载设置
        this.loadSettings();

        // 启动页停留 1.5 秒
        setTimeout(() => {
            this.currentPage = 'wish';
        }, 1500);

        // 监听设备运动（摇一摇）
        if (this.isMobile && window.DeviceMotionEvent) {
            this.requestMotionPermission();
        }
    },

    methods: {
        // ==================== 数据加载 ====================

        async loadFortunes() {
            try {
                // 使用浅草寺签文数据
                const response = await fetch('data/senso-ji-fortunes-full.json');
                const data = await response.json();
                this.allFortunes = data.fortunes.map(fortune => {
                    return {
                        ...fortune,
                        level: this.convertLevelToChinese(fortune.level),
                        formattedId: this.formatFortuneId(fortune.id),
                        shortDescription: fortune.poem.lines[0]
                    };
                });
                console.log(`✅ 已加载 ${this.allFortunes.length} 条浅草寺签文`);
                console.log(`📊 签级分布: ${JSON.stringify(data.metadata.distribution)}`);
            } catch (error) {
                console.error('❌ 加载签文失败:', error);
                this.showToast('加载签文数据失败', 'error');
            }
        },

        // 将英文签级转换为中文（浅草寺签级体系）
        convertLevelToChinese(level) {
            const mapping = {
                'excellent': '大吉',   // 浅草寺大吉
                'good': '吉',          // 浅草寺吉
                'medium': '半吉',      // 浅草寺半吉
                'small': '小吉',       // 浅草寺小吉
                '末吉': '末吉',        // 浅草寺末吉
                'poor': '凶',          // 浅草寺凶
                'worst': '大凶',       // 浅草寺大凶
                // 兼容旧数据
                'supreme': '大吉',
            };
            return mapping[level] || level;
        },

        loadHistory() {
            const saved = localStorage.getItem('fortuneHistory');
            if (saved) {
                this.history = JSON.parse(saved);
                console.log(`📜 加载了 ${this.history.length} 条历史记录`);
            }
        },

        loadSettings() {
            const saved = localStorage.getItem('appSettings');
            if (saved) {
                this.settings = { ...this.settings, ...JSON.parse(saved) };
            }
        },

        // ==================== 摇一摇检测 ====================

        async requestMotionPermission() {
            // iOS 13+ 需要请求权限
            if (typeof DeviceMotionEvent.requestPermission === 'function') {
                try {
                    const permission = await DeviceMotionEvent.requestPermission();
                    if (permission === 'granted') {
                        this.startShakeDetection();
                    } else {
                        console.log('❌ 用户拒绝了运动传感器权限');
                    }
                } catch (error) {
                    console.error('❌ 请求权限失败:', error);
                }
            } else {
                // 非 iOS 或旧版本，直接启动
                this.startShakeDetection();
            }
        },

        startShakeDetection() {
            window.addEventListener('devicemotion', this.handleDeviceMotion);
            console.log('✅ 摇一摇检测已启动');
        },

        handleDeviceMotion(event) {
            if (this.currentPage !== 'shake' || this.isShaking) return;

            const acc = event.accelerationIncludingGravity;
            const current = Math.abs(acc.x) + Math.abs(acc.y) + Math.abs(acc.z);

            // 检测加速度变化
            const now = Date.now();
            if (current > this.shakeThreshold && now - this.lastShakeTime > 800) {
                this.lastShakeTime = now;
                this.onShake();
            }
        },

        simulateShake() {
            this.onShake();
        },

        onShake() {
            console.log('🎲 检测到摇动！');
            this.isShaking = true;

            // 震动反馈
            this.vibrate();

            // 0.8 秒后抽签
            setTimeout(() => {
                this.drawFortune();
                this.isShaking = false;
            }, 800);
        },

        // ==================== 抽签逻辑 ====================

        drawFortune() {
            if (this.allFortunes.length === 0) {
                this.showToast('签文数据未加载', 'error');
                return;
            }

            // 🎲 构建加权抽签池：凶和末小吉概率减半
            // 吉祥签（大吉、吉、末吉、小吉、半吉）：权重 2（添加2次）
            // 凶签（凶、末小吉）：权重 1（添加1次，概率减半）
            const weightedPool = [];

            const unluckyLevels = ['凶', '末小吉'];

            for (const fortune of this.allFortunes) {
                // 凶签只添加一次（权重1）
                if (unluckyLevels.includes(fortune.level)) {
                    weightedPool.push(fortune);
                }
                // 吉祥签添加两次（权重2）
                else {
                    weightedPool.push(fortune);
                    weightedPool.push(fortune);
                }
            }

            if (weightedPool.length === 0) {
                this.showToast('没有可用的签文', 'error');
                return;
            }

            // 使用时间戳和随机数混合
            const timestamp = Date.now();
            const randomIndex = Math.floor(Math.random() * weightedPool.length);
            const seed = (timestamp % 1000) + randomIndex;
            const finalIndex = seed % weightedPool.length;

            const fortune = { ...weightedPool[finalIndex] };
            fortune.timestamp = new Date().toISOString();
            fortune.formattedTime = this.formatTime(new Date());

            if (this.userWish) {
                fortune.wish = this.userWish;
            }

            this.currentFortune = fortune;

            // 保存到历史
            this.saveToHistory(fortune);

            // 震动反馈
            this.vibrate('success');

            console.log(`🎊 抽中第 ${fortune.id} 签 - ${fortune.level}`);

            // 跳转到签文页
            setTimeout(() => {
                this.goToPage('fortune');
            }, 300);
        },

        // ==================== 页面导航 ====================

        goToPage(page) {
            this.previousPage = this.currentPage;
            this.currentPage = page;

            // 进入签文页时重置图片显示状态
            if (page === 'fortune') {
                this.showImageSide = 'front';
            }
        },

        goBack() {
            if (this.previousPage) {
                this.currentPage = this.previousPage;
                this.previousPage = '';
            } else {
                this.currentPage = 'shake';
            }
        },

        skipWish() {
            this.userWish = '';
            this.goToPage('shake');
        },

        goToShake() {
            this.userWish = '';
            this.goToPage('shake');
        },

        goToHistory() {
            this.goToPage('history');
        },

        drawAgain() {
            this.userWish = '';
            this.currentFortune = null;
            this.goToPage('wish');
        },

        viewHistoryFortune(fortune) {
            this.currentFortune = fortune;
            this.goToPage('fortune');
        },

        // ==================== 历史记录管理 ====================

        saveToHistory(fortune) {
            this.history.unshift(fortune);

            // 限制最多 100 条
            if (this.history.length > 100) {
                this.history = this.history.slice(0, 100);
            }

            localStorage.setItem('fortuneHistory', JSON.stringify(this.history));
        },

        confirmClearHistory() {
            if (confirm('确定要清空所有历史记录吗？')) {
                this.clearHistory();
            }
        },

        clearHistory() {
            this.history = [];
            localStorage.removeItem('fortuneHistory');
            this.showToast('已清空历史记录');
        },

        // ==================== 设置管理 ====================

        saveSettings() {
            localStorage.setItem('appSettings', JSON.stringify(this.settings));
        },

        showAbout() {
            alert('一念 v1.0.0\n\n一款禅意极简风格的摇签应用\n\n© 2026');
        },

        // ==================== 工具方法 ====================

        getLevelColor(level) {
            return this.levelColors[level] || '#73706A';
        },

        formatFortuneId(id) {
            const chineseNumbers = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九'];

            if (id < 10) {
                return `第${chineseNumbers[id]}签`;
            } else if (id === 10) {
                return '第十签';
            } else if (id < 20) {
                return `第十${chineseNumbers[id % 10]}签`;
            } else {
                const tens = Math.floor(id / 10);
                const ones = id % 10;
                if (ones === 0) {
                    return `第${chineseNumbers[tens]}十签`;
                } else {
                    return `第${chineseNumbers[tens]}十${chineseNumbers[ones]}签`;
                }
            }
        },

        formatTime(date) {
            const d = new Date(date);
            const year = d.getFullYear();
            const month = String(d.getMonth() + 1).padStart(2, '0');
            const day = String(d.getDate()).padStart(2, '0');
            const hours = String(d.getHours()).padStart(2, '0');
            const minutes = String(d.getMinutes()).padStart(2, '0');
            return `${year}.${month}.${day} ${hours}:${minutes}`;
        },

        vibrate(type = 'medium') {
            if (!this.settings.haptic || !navigator.vibrate) return;

            const patterns = {
                light: 10,
                medium: 20,
                heavy: 30,
                success: [10, 50, 10]
            };

            navigator.vibrate(patterns[type] || 20);
        },

        showToast(message, type = 'info') {
            this.toast.message = message;
            this.toast.type = type;
            this.toast.show = true;

            setTimeout(() => {
                this.toast.show = false;
            }, 2000);
        },

        // ==================== 图片查看 ====================

        showImageFullscreen(imagePath) {
            this.fullscreenImage = 'data/' + imagePath;
        },

        closeFullscreen() {
            this.fullscreenImage = null;
        },

        shareFortune() {
            if (!this.currentFortune) return;

            const text = `我在「一念」抽到了：\n${this.currentFortune.formattedId} ${this.currentFortune.level}\n\n${this.currentFortune.poem.lines.join('\n')}`;

            if (navigator.share) {
                navigator.share({
                    title: '一念 - 摇签',
                    text: text
                }).catch(err => console.log('分享失败:', err));
            } else {
                // 复制到剪贴板
                this.copyToClipboard(text);
                this.showToast('已复制到剪贴板');
            }

            this.showMenu = false;
        },

        copyToClipboard(text) {
            const textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
        }
    },

    watch: {
        // 监听设置变化并保存
        settings: {
            handler() {
                this.saveSettings();
            },
            deep: true
        }
    }
}).mount('#app');
