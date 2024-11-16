document.getElementById('searchInput').addEventListener('input', function() {
    const filter = this.value.toLowerCase();
    const dishItems = document.querySelectorAll('.dish-item');

    dishItems.forEach(item => {
        const dishName = item.querySelector('.card-title').innerText.toLowerCase();
        if (dishName.includes(filter)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
});

document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        const url = this.getAttribute('data-url');

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                document.getElementById('errorModalBody').innerText = data.message;
                $('#errorModal').modal('show');
            } else {
                window.location.href = this.getAttribute('href');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
