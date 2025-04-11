// Функция для переключения видимости сайдбара
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const menuBtn = document.getElementById('menu-btn');
    
    // Проверяем размер экрана
    const isMobile = window.innerWidth <= 992;
    
    if (isMobile) {
        // На мобильных устройствах используем класс visible
        sidebar.classList.toggle('visible');
    } else {
        // На десктопе переключаем между видимым и скрытым сайдбаром
        sidebar.classList.toggle('hidden');
        mainContent.classList.toggle('full-width');
        menuBtn.classList.toggle('sidebar-visible');
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const menuBtn = document.getElementById('menu-btn');

    // Убедимся, что элементы существуют
    if (sidebar && mainContent && menuBtn) {
        // Если экран мобильный, скрываем сайдбар по умолчанию
        if (window.innerWidth <= 992) {
            sidebar.classList.remove('hidden');
            sidebar.classList.remove('visible'); // Сайдбар должен быть скрыт изначально на мобильных
            mainContent.classList.add('full-width');
        } else {
            // На десктопе показываем сайдбар по умолчанию
            sidebar.classList.remove('hidden');
            mainContent.classList.remove('full-width');
            menuBtn.classList.add('sidebar-visible'); // Добавляем этот класс на десктопе
        }
    }
});

// Обработка изменения размера окна - исправленная версия
window.addEventListener('resize', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const menuBtn = document.getElementById('menu-btn');

    // Проверяем, что элементы существуют
    if (sidebar && mainContent && menuBtn) {
        const isMobile = window.innerWidth <= 992;

        if (isMobile) {
            // Переключаемся на мобильный режим
            sidebar.classList.remove('hidden');
            // Сохраняем класс visible если он был, чтобы не скрывать уже открытый сайдбар
            mainContent.classList.add('full-width');
            menuBtn.classList.remove('sidebar-visible');
        } else {
            // Переключаемся на десктопный режим
            sidebar.classList.remove('visible');
            // Проверяем, должен ли сайдбар быть скрытым
            if (!sidebar.classList.contains('hidden')) {
                mainContent.classList.remove('full-width');
                menuBtn.classList.add('sidebar-visible');
            }
        }
    }
});