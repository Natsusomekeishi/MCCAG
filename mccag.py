<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="static/logo.png">
    <title>Minecraft CAG</title>
    <meta name="description" content="Minecraft Cute Avatar Generator（MCCAG）是一款专为Minecraft玩家设计的头像生成工具。通过这款工具，你可以轻松地制作出属于你自己的可爱头像，支持多种背景颜色选择和高清保存。">
    <meta name="keywords" content="Minecraft, Avatar Generator, MCCAG, Minecraft头像生成器, 可爱头像, 个性化头像, 高清头像, Minecraft工具">
    <meta name="author" content="Keishi">
    <script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>
    <script type="text/javascript" src="https://cdn.repository.webfont.com/wwwroot/js/wf/youziku.api.min.js"></script>
    <script type="text/javascript">
       $webfont.load("body", "1c66cdcc6b0b44e9b05f503978baee36", "Source-Han-Sans-Medium");
       /*$webfont.load("#id1,.class1,h1", "1c66cdcc6b0b44e9b05f503978baee36", "Source-Han-Sans-Medium");*/
       /*．．．*/
       $webfont.draw();
    </script>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f2f5;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            height: 100%;
            width: 100%;
            box-sizing: border-box;
        }
        .header img {
            margin-top: -7px;
            height: 55px;
        }
        h1 {
            margin-left: 10px;
            margin-top: 16px;
        }
        .header-left {
            display: flex;
            align-items: center;
            margin-left: 50px;
        }
        .header {
            height: 70px;
            top: 0;
            background-color: #007bff;
            color: white;
            text-align: center;
            width: 100%;
            left: 0;
        }
        .footer {
            background-color: #007bff;
            color: white;
            text-align: center;
            padding: 10px 20px;
            width: 100%;
            left: 0;
            position: fixed;
            bottom: 0;
            font-size: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
        }
        .footer a {
            color: #fff;
            text-decoration: none;
            padding: 5px 10px;
            background-color: #28a745;
            border-radius: 5px;
            transition: background-color 0.3s;
            margin-right: 50px;
        }
        .footer a:hover {
            background-color: #218838;
        }
        .container-wrapper {
            display: flex;
            flex-direction: column;
            gap: 20px;
            max-width: 1200px;
            margin: 50px auto;
            padding: 0 20px;
            margin-bottom: 80px;
        }
        .container {
            background: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            max-width: 400px;
            width: 90%;
            margin: 0 auto; 
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 50px;
        }
        h2 {
            font-size: 20px;
            color: #333;
            margin-bottom: 20px;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
            width: 100%;
        }
        input[type="text"] {
            padding: 10px;
            font-size: 16px;
            border: 1px solid #dcdcdc;
            border-radius: 5px;
            outline: none;
            transition: border-color 0.3s;
            height: 50px;
            text-align: center;
        }
        
        input[type="text"]::placeholder {
            text-align: center; 
            font-size: 20px; 
        }        
        input[type="text"]:focus {
            border-color: #007bff;
        }
        button {
            padding: 10px;
            font-size: 16px;
            color: #fff;
            background-color: #007bff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 20px;
            text-align: center;
        }
        .result img {
            max-width: 100%;
            height: auto;
            display: none;
        }
        .result h2 {
            color: #333;
            margin-bottom: 10px;
        }
        .download-btn {
            margin-top: 15px;
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: #fff;
            background-color: #28a745;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            transition: background-color 0.3s;
            margin-right: 20px;
            margin-left: 20px;
        }
        .download-btn:hover {
            background-color: #218838;
        }
        #avatar-canvas {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            border: 2px solid #007bff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .nav-buttons {
            display: flex;
            margin-top: 10px;
            justify-content: center;
        }
        .nav-buttons button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .nav-buttons button:hover {
            background-color: #0056b3;
        }
        #prev-btn, #next-btn {
            margin-top: 15px;
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: #fff;
            background-color: #28a745;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            transition: background-color 0.3s;
        }

        #prev-btn:hover, #next-btn:hover {
            background-color: #218838;
        }
        p a {
            text-decoration: none; 
            color: #007bff;
            font-size: 20px;
            font-weight: bold;
        }
        
        p a:visited {
            color: #007bff;
        }
        
        p a:hover {
            color: #007bff;
        }
        
        #text {
            padding-top: 30px;
            padding-bottom: 30px;
            height: 600px;
        }
        
        #text img {
            border-radius: 10px;
            border: 2px solid #007bff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        /* 媒体查询: 适用于PC和iPad */
        @media (min-width: 768px) {
            .container-wrapper {
                flex-direction: row;
            }
            .container {
                margin: 0 20px; /* 左右间距 */
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-left">
            <img src="static/logo.png" alt="Logo">
            <h1>MC头像生成器</h1>
        </div>
    </div>
    <div class="container-wrapper">
        <div class="container">
            <form action="/" method="post">
                <input type="text" id="username" name="username" placeholder="输入正版玩家ID" required>
                <button type="submit">生成头像</button>
            </form>
            <div class="result">
                <div id="avatar-container" style="position: relative; display: inline-block;">
                    <canvas id="avatar-canvas"></canvas>
                    <img id="avatar-image" src="{{ image_url or url_for('static', filename='cache/923ed5ce249a4cd3ac7d23e6797b939c.png') }}" alt="MC 头像">
                </div>
                <div class="nav-buttons">
                    <button id="prev-btn">&lt;</button>
                    <a id="download-btn" class="download-btn" href="#">下载头像</a>
                    <button id="next-btn">&gt;</button>
                </div>
            </div>
        </div>
        <div class="container" id="text">
            <p>网站作者：<a href="https://space.bilibili.com/23785358/" target="_blank">Keishi</a>&nbsp;&nbsp;赞助：DongYue</p>
            <p>灵感来源：<a href="https://www.bilibili.com/video/BV1rB4y1F7dW/" target="_blank">噪音回放（B站视频链接）</a></p>
            <p><a href="https://afdian.com/a/Keishi" target="_blank">☕给作者一杯咖啡支持一下~</a></p>
            <p>本网站纯公益，请勿利用该网站制品贩卖！</p>
            <p>右下角爱发电动态有更新计划，会尽快适配旧版皮肤~</p>
            <p>某不知名1.21纯生存服务器宣传：<a href="https://qm.qq.com/q/8cT2Gdgbg4" target="_blank">796461662</a></p>
            <p><img src="static/image.jpg" height="230px"></p>
        </div>
    </div>
    <div class="footer">
        <a href="https://github.com/Natsusomekeishi/MCCAG" target="_blank">Github</a>
        <span style="text-align: center; margin-right: 40px;">网站总访问量&nbsp;<strong><span id="busuanzi_value_site_pv"></span></strong>&nbsp;次</span>
        <a href="https://afdian.com/a/Keishi" target="_blank">打赏一下</a>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const avatarImage = document.getElementById('avatar-image');
            const avatarCanvas = document.getElementById('avatar-canvas');
            const ctx = avatarCanvas.getContext('2d');
            const downloadBtn = document.getElementById('download-btn');
            const prevBtn = document.getElementById('prev-btn');
            const nextBtn = document.getElementById('next-btn');

            const backgrounds = [
                "#ffcccb",
                "#add8e6",
                "#ffffff",
                "linear-gradient(135deg, #ffcccb 0%, #ffeb3b 100%)",
                "linear-gradient(135deg, #f1eef9 0%, #f5ccf6 100%)",
                "linear-gradient(135deg, #d4fc78 0%, #99e5a2 100%)",
                "linear-gradient(135deg, #41d8dd 0%, #5583ee 100%)",
                "linear-gradient(135deg, #323b42 0%, #121317 100%)"
                
            ];
            let currentBackgroundIndex = 0;

            function updateCanvas() {
                const backgroundColor = backgrounds[currentBackgroundIndex];
                
                const displayWidth = 1000; // 设置显示宽度
                const scaleFactor = displayWidth / avatarImage.width;
                const displayHeight = avatarImage.height * scaleFactor;

                avatarCanvas.width = displayWidth;
                avatarCanvas.height = displayHeight;

                // 填充背景颜色
                if (backgroundColor.startsWith("linear-gradient")) {
                    const gradient = ctx.createLinearGradient(0, 0, avatarCanvas.width, avatarCanvas.height);
                    const colors = backgroundColor.match(/#\w{6}/g);
                    gradient.addColorStop(0, colors[0]);
                    gradient.addColorStop(1, colors[1]);
                    ctx.fillStyle = gradient;
                } else {
                    ctx.fillStyle = backgroundColor;
                }
                ctx.fillRect(0, 0, avatarCanvas.width, avatarCanvas.height);

                // 绘制头像
                ctx.drawImage(avatarImage, 0, 0, displayWidth, displayHeight);
            }

            // 初始化画布
            avatarImage.onload = function() {
                updateCanvas();
            }

            // 切换背景颜色
            prevBtn.addEventListener('click', function() {
                currentBackgroundIndex = (currentBackgroundIndex - 1 + backgrounds.length) % backgrounds.length;
                updateCanvas();
            });

            nextBtn.addEventListener('click', function() {
                currentBackgroundIndex = (currentBackgroundIndex + 1) % backgrounds.length;
                updateCanvas();
            });

            // 下载图像
            downloadBtn.addEventListener('click', function(event) {
                event.preventDefault();
                const link = document.createElement('a');
                link.download = 'mc_avatar.png';
                link.href = avatarCanvas.toDataURL('image/png');
                link.click();
            });

            // 如果头像图片已经加载完毕，立即更新画布
            if (avatarImage.complete) {
                updateCanvas();
            }
        });
    </script>
</body>
</html>
