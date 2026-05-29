const examItems = document.querySelectorAll('.exam-item');
examItems.forEach(item => {
    item.style.display = 'flex';
    item.style.alignItems = 'center';
    item.style.justifyContent = 'space-between';
    item.style.padding = '1rem';
    item.style.border = '1px solid var(--border)';
    item.style.borderRadius = 'var(--radius)';
    item.style.marginBottom = '1rem';
});