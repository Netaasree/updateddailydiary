// Save diary functionality
document.getElementById('save-diary-btn')?.addEventListener('click', function() {
    const content = document.getElementById('diary-content')?.value;

    fetch('http://127.0.0.1:5000/diary', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            content: content
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById('diary-content').value = '';
            document.getElementById('save-message').textContent = 'Diary is saved!';
            document.getElementById('save-message').classList.remove('hidden');
        } else {
            alert(data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});

// Load diaries functionality
function loadDiaries() {
    fetch('http://127.0.0.1:5000/diaries')
    .then(response => response.json())
    .then(data => {
        const diaryList = document.getElementById('diary-list');
        diaryList.innerHTML = '';
        data.forEach(diary => {
            const li = document.createElement('li');
            li.textContent = diary.content;
            diaryList.appendChild(li);
        });
    })
    .catch(error => console.error('Error:', error));
}

// Load existing diary entries on page load for diaries.html
if (document.getElementById('diary-list')) {
    loadDiaries();
}