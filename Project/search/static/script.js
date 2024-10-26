document.getElementById('search-box').addEventListener('input', function() {
    const query = this.value;
    const searchResults = document.getElementById('search-results');

    if (query.length > 0) {
        fetch(`/search/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                searchResults.innerHTML = '';
                data.forEach(stock => {
                    const div = document.createElement('div');
                    div.textContent = `${stock.Symbol} - ${stock.Tên}`;
                    div.addEventListener('click', () => {
                        alert(`Selected stock: ${stock.Symbol}`);
                    });
                    searchResults.appendChild(div);
                });
                searchResults.style.display = 'block';
            })
            .catch(error => {
                console.error('Error fetching search results:', error);
                searchResults.style.display = 'none';
            });
    } else {
        searchResults.style.display = 'none';
    }
});
