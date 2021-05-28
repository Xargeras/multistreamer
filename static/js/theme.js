function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    document.documentElement.className = themeName;
}

function toggleTheme() {
    if (localStorage.getItem('theme') === 'theme-dark') {
        setTheme('theme-light');
    } else {
        setTheme('theme-dark');
    }
}

(function () {
    if (localStorage.getItem('theme') === 'theme-dark') {
        console.log($('#theme_swap'))
        setTheme('theme-dark');
        $('#theme_swap').prop('checked', false)
    } else {
        setTheme('theme-light');
        $('#theme_swap').prop('checked', true)
    }
})();
