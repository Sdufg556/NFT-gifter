from flask import Flask, jsonify, request
import random
import json
import os

app = Flask(__name__)

# Простая база данных в файле
DB_FILE = 'database.json'

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {'users': {}, 'gifts': []}

def save_db(db):
    with open(DB_FILE, 'w') as f:
        json.dump(db, f)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🎁 NFT Gifter</title>
        <meta name="telegram:site" content="@your_bot">
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                color: #333;
            }
            
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.98);
                border-radius: 25px;
                padding: 30px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            
            header {
                text-align: center;
                margin-bottom: 40px;
                padding-bottom: 25px;
                border-bottom: 3px solid #f0f0f0;
            }
            
            h1 {
                color: #333;
                font-size: 2.8rem;
                margin-bottom: 20px;
                background: linear-gradient(45deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            .user-panel {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .stars-badge {
                background: linear-gradient(45deg, #FFD700, #FFA500);
                padding: 15px 30px;
                border-radius: 50px;
                font-size: 1.8rem;
                font-weight: bold;
                color: #333;
                box-shadow: 0 5px 15px rgba(255,215,0,0.4);
            }
            
            .section {
                margin: 50px 0;
            }
            
            h2 {
                color: #444;
                font-size: 2rem;
                margin-bottom: 25px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .gifts-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 25px;
                margin-top: 20px;
            }
            
            .gift-card {
                background: white;
                border-radius: 20px;
                padding: 25px;
                text-align: center;
                border: 3px solid #e0e0e0;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .gift-card:hover {
                transform: translateY(-8px);
                border-color: #667eea;
                box-shadow: 0 15px 30px rgba(102,126,234,0.2);
            }
            
            .gift-icon {
                font-size: 4.5rem;
                margin-bottom: 20px;
            }
            
            .gift-card h3 {
                color: #333;
                font-size: 1.5rem;
                margin-bottom: 10px;
            }
            
            .gift-price {
                color: #FF8C00;
                font-size: 1.6rem;
                font-weight: bold;
                margin: 15px 0;
            }
            
            .buy-btn {
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                border: none;
                padding: 14px 25px;
                border-radius: 25px;
                font-size: 1.2rem;
                font-weight: bold;
                width: 100%;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-top: 10px;
            }
            
            .buy-btn:hover {
                transform: scale(1.05);
                box-shadow: 0 8px 20px rgba(102,126,234,0.3);
            }
            
            .my-gifts-container {
                background: rgba(248, 249, 250, 0.7);
                border-radius: 20px;
                padding: 25px;
                margin-top: 20px;
                border: 2px dashed #667eea;
            }
            
            .my-gift-item {
                background: white;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 15px;
                border-left: 5px solid #667eea;
            }
            
            .gift-details {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
                margin-top: 15px;
                font-size: 0.9rem;
            }
            
            .gift-detail {
                background: #f8f9fa;
                padding: 8px;
                border-radius: 8px;
                text-align: center;
            }
            
            .upgrade-btn {
                background: #28a745;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 20px;
                cursor: pointer;
                margin-top: 15px;
                width: 100%;
                font-weight: bold;
            }
            
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: #28a745;
                color: white;
                padding: 15px 25px;
                border-radius: 10px;
                display: none;
                z-index: 1000;
            }
            
            @media (max-width: 600px) {
                .container {
                    padding: 20px;
                    border-radius: 20px;
                }
                
                h1 {
                    font-size: 2.2rem;
                }
                
                .gifts-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="notification" id="notification"></div>
        
        <div class="container">
            <header>
                <h1>🎁 NFT Gifter</h1>
                <p style="color: #666; font-size: 1.2rem; margin-bottom: 25px;">
                    Покупай и улучшай подарки, наслаждайся ботом :)
                </p>
                
                <div class="user-panel">
                    <div class="stars-badge">
                        ⭐ <span id="star-count">100</span>
                    </div>
                </div>
            </header>
            
            <main>
                <section class="section">
                    <h2>🛍️ Магазин подарков</h2>
                    <p style="color: #666; margin-bottom: 20px; font-style: italic;">
                        Оставь тут свои звёздочки :)
                    </p>
                    
                    <div class="gifts-grid" id="shop-gifts">
                        <!-- Подарки загружаются через JS -->
                    </div>
                </section>
                
                <section class="section">
                    <h2>🎀 Ваши подарки</h2>
                    <div class="my-gifts-container" id="my-gifts">
                        <!-- Подарки пользователя -->
                    </div>
                </section>
            </main>
        </div>
        
        <script>
            // Telegram Mini App
            const tg = window.Telegram?.WebApp;
            let userId = 'user_' + Math.random().toString(36).substr(2, 9);
            
            if (tg) {
                tg.expand();
                tg.MainButton.text = "Вернуться в бот";
                tg.MainButton.show();
                userId = tg.initDataUnsafe?.user?.id || userId;
            }
            
            const backendUrl = window.location.origin;
            let userStars = 100;
            
            // Магазин подарков
            const shopGifts = [
                { id: 1, type: 'basic', name: 'Базовый подарок', price: 50, emoji: '🎁', color: '#4CAF50' },
                { id: 2, type: 'premium', name: 'Премиум подарок', price: 150, emoji: '💎', color: '#2196F3' },
                { id: 3, type: 'legendary', name: 'Легендарный подарок', price: 500, emoji: '👑', color: '#FF9800' },
                { id: 4, type: 'special', name: 'Особый подарок', price: 300, emoji: '✨', color: '#9C27B0' }
            ];
            
            // Инициализация
            async function init() {
                await loadUserData();
                renderShop();
            }
            
            // Загружаем данные пользователя
            async function loadUserData() {
                try {
                    const response = await fetch(`/api/user/${userId}`);
                    const data = await response.json();
                    
                    userStars = data.stars || 100;
                    document.getElementById('star-count').textContent = userStars;
                    
                    if (data.gifts && data.gifts.length > 0) {
                        renderUserGifts(data.gifts);
                    } else {
                        document.getElementById('my-gifts').innerHTML = 
                            '<p style="text-align: center; color: #666; padding: 40px;">У вас пока нет подарков. Купите первый!</p>';
                    }
                } catch (error) {
                    console.error('Ошибка загрузки:', error);
                }
            }
            
            // Показываем магазин
            function renderShop() {
                const container = document.getElementById('shop-gifts');
                container.innerHTML = '';
                
                shopGifts.forEach(gift => {
                    const card = document.createElement('div');
                    card.className = 'gift-card';
                    card.innerHTML = `
                        <div class="gift-icon">${gift.emoji}</div>
                        <h3>${gift.name}</h3>
                        <div class="gift-price">${gift.price} ⭐</div>
                        <button class="buy-btn" onclick="buyGift('${gift.type}')" 
                                ${userStars < gift.price ? 'disabled style="opacity: 0.5;"' : ''}>
                            ${userStars < gift.price ? 'Недостаточно звезд' : 'Купить'}
                        </button>
                    `;
                    container.appendChild(card);
                });
            }
            
            // Покупаем подарок
            async function buyGift(giftType) {
                const gift = shopGifts.find(g => g.type === giftType);
                
                if (userStars < gift.price) {
                    showNotification('Недостаточно звезд!', 'error');
                    return;
                }
                
                if (!confirm(`Купить ${gift.name} за ${gift.price} звезд?`)) return;
                
                try {
                    const response = await fetch(`/api/buy/${userId}/${giftType}`, {
                        method: 'POST'
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        showNotification('🎉 Подарок успешно куплен!', 'success');
                        userStars = result.stars;
                        document.getElementById('star-count').textContent = userStars;
                        await loadUserData();
                        renderShop();
                    } else {
                        showNotification(result.message || 'Ошибка покупки', 'error');
                    }
                } catch (error) {
                    showNotification('Ошибка соединения', 'error');
                    console.error(error);
                }
            }
            
            // Показываем подарки пользователя
            function renderUserGifts(gifts) {
                const container = document.getElementById('my-gifts');
                container.innerHTML = '';
                
                gifts.forEach(gift => {
                    const item = document.createElement('div');
                    item.className = 'my-gift-item';
                    item.innerHTML = `
                        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                            <div style="font-size: 3rem;">${getGiftEmoji(gift.type)}</div>
                            <div>
                                <h3 style="margin: 0;">${getGiftName(gift.type)}</h3>
                                <p style="color: #666; margin: 5px 0;">Уровень: ${gift.level}</p>
                            </div>
                        </div>
                        
                        <div class="gift-details">
                            <div class="gift-detail">🎨 ${gift.pattern}</div>
                            <div class="gift-detail">🖼️ ${gift.background}</div>
                            <div class="gift-detail">🎲 Редкость: ${gift.rarity || 'обычная'}</div>
                            <div class="gift-detail">#${gift.id}</div>
                        </div>
                        
                        <button class="upgrade-btn" onclick="upgradeGift(${gift.id})">
                            Улучшить (25 ⭐)
                        </button>
                    `;
                    container.appendChild(item);
                });
            }
            
            // Улучшаем подарок
            async function upgradeGift(giftId) {
                if (userStars < 25) {
                    showNotification('Недостаточно звезд для улучшения!', 'error');
                    return;
                }
                
                try {
                    const response = await fetch(`/api/upgrade/${userId}/${giftId}`, {
                        method: 'POST'
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        showNotification('✨ Подарок улучшен!', 'success');
                        userStars = result.stars;
                        document.getElementById('star-count').textContent = userStars;
                        await loadUserData();
                    }
                } catch (error) {
                    showNotification('Ошибка улучшения', 'error');
                }
            }
            
            // Вспомогательные функции
            function getGiftEmoji(type) {
                const emojis = { basic: '🎁', premium: '💎', legendary: '👑', special: '✨' };
                return emojis[type] || '🎁';
            }
            
            function getGiftName(type) {
                const names = { basic: 'Базовый', premium: 'Премиум', legendary: 'Легендарный', special: 'Особый' };
                return names[type] || 'Подарок';
            }
            
            function showNotification(message, type = 'success') {
                const notification = document.getElementById('notification');
                notification.textContent = message;
                notification.style.background = type === 'success' ? '#28a745' : '#dc3545';
                notification.style.display = 'block';
                
                setTimeout(() => {
                    notification.style.display = 'none';
                }, 3000);
            }
            
            // Запускаем приложение
            document.addEventListener('DOMContentLoaded', init);
        </script>
    </body>
    </html>
    '''

@app.route('/api/user/<user_id>')
def get_user(user_id):
    db = load_db()
    
    if user_id not in db['users']:
        db['users'][user_id] = {
            'stars': 1000,
            'gifts': []
        }
        save_db(db)
    
    user_gifts = [g for g in db['gifts'] if g['owner_id'] == user_id]
    
    return jsonify({
        'stars': db['users'][user_id]['stars'],
        'gifts': user_gifts
    })

@app.route('/api/buy/<user_id>/<gift_type>', methods=['POST'])
def buy_gift(user_id, gift_type):
    db = load_db()
    
    if user_id not in db['users']:
        db['users'][user_id] = {'stars': 1000, 'gifts': []}
    
    # Цены подарков
    prices = {'basic': 50, 'premium': 150, 'legendary': 500, 'special': 300}
    price = prices.get(gift_type, 50)
    
    if db['users'][user_id]['stars'] < price:
        return jsonify({'success': False, 'message': 'Недостаточно звезд'})
    
    # Списываем звезды
    db['users'][user_id]['stars'] -= price
    
    # Создаем подарок
    gift_id = len(db['gifts']) + 1
    
    patterns = ["Сердца", "Звезды", "Полосы", "Точки", "Волны", "Геометрия"]
    backgrounds = ["Синий", "Красный", "Золотой", "Космос", "Радуга", "Неон"]
    rarities = ["Обычный", "Редкий", "Эпический", "Легендарный"]
    
    new_gift = {
        'id': gift_id,
        'owner_id': user_id,
        'type': gift_type,
        'level': 1,
        'pattern': random.choice(patterns),
        'background': random.choice(backgrounds),
        'rarity': random.choices(rarities, weights=[50, 30, 15, 5])[0],
        'created_at': '2024-01-01'
    }
    
    db['gifts'].append(new_gift)
    save_db(db)
    
    return jsonify({
        'success': True,
        'gift': new_gift,
        'stars': db['users'][user_id]['stars'],
        'message': 'Подарок куплен!'
    })

@app.route('/api/upgrade/<user_id>/<int:gift_id>', methods=['POST'])
def upgrade_gift(user_id, gift_id):
    db = load_db()
    
    if db['users'][user_id]['stars'] < 25:
        return jsonify({'success': False, 'message': 'Недостаточно звезд'})
    
    # Находим подарок
    for gift in db['gifts']:
        if gift['id'] == gift_id and gift['owner_id'] == user_id:
            gift['level'] += 1
            db['users'][user_id]['stars'] -= 25
            save_db(db)
            
            return jsonify({
                'success': True,
                'level': gift['level'],
                'stars': db['users'][user_id]['stars']
            })
    
    return jsonify({'success': False, 'message': 'Подарок не найден'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
