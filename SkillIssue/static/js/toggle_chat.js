document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('floating-button');
    const modal = document.getElementById('chat-modal');
    const closeButton = document.getElementById('chat-close-button');
    const backToChats = document.getElementById('back-to-chats');
    const chatContacts = document.getElementById('chat-contacts');
    const chatDialog = document.getElementById('chat-dialog');
    const profileLink = document.getElementById('profile-link');
    const messagesContainer = document.getElementById('messages-container');

    // Открытие модального окна
    button.addEventListener('click', function () {
        modal.style.right = '20px';
    });

    // Закрытие модального окна
    closeButton.addEventListener('click', function () {
        modal.style.right = '-400px';
    });

    // Переход к диалогу
    document.querySelectorAll('.chat-item').forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();

            const username = this.querySelector('.username').textContent;
            const userId = this.getAttribute('data-user-id');

            // Обновляем заголовок диалога
            profileLink.textContent = username;
            profileLink.href = `/profiles/${userId}/`; // ссылка на профиль

            // Очищаем предыдущие сообщения (в реальной версии — подгружайте из API)
            messagesContainer.innerHTML = '';

            // Пример сообщений (в будущем — из Django API)
            if (userId === '1') {
                addMessage('received', 'Привет! Как продвигается проект?', '12:30');
                addMessage('sent', 'Всё хорошо, почти готов!', '12:31');
            } else if (userId === '2') {
                addMessage('received', 'Не забудь добавить тесты.', '14:20');
                addMessage('sent', 'Конечно, сделаю сегодня.', '14:22');
            }

            // Показываем диалог
            chatContacts.style.display = 'none';
            chatDialog.style.display = 'flex';
        });
    });

    // Возврат к списку
    backToChats.addEventListener('click', function () {
        chatDialog.style.display = 'none';
        chatContacts.style.display = 'flex';
    });

    // Функция для добавления сообщения
    function addMessage(type, text, time) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.style.cssText = type === 'sent'
            ? "max-width: 70%; background: #007bff; color: white; padding: 10px 15px; border-radius: 18px 18px 4px 18px; align-self: flex-end; box-shadow: 0 1px 3px rgba(0,0,0,0.1);"
            : "max-width: 70%; background: white; padding: 10px 15px; border-radius: 18px 18px 18px 4px; align-self: flex-start; box-shadow: 0 1px 3px rgba(0,0,0,0.1);";

        messageDiv.innerHTML = `
            <div class="message-text" style="font-size: 0.95rem; ${type === 'sent' ? 'color: white;' : 'color: #333;'}">${text}</div>
            <div class="message-time" style="font-size: 0.75rem; ${type === 'sent' ? 'color: rgba(255,255,255,0.8);' : 'color: #999;'} text-align: right; margin-top: 4px;">${time}</div>
        `;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
});