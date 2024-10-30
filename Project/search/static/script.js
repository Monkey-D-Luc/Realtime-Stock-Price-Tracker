document.getElementById('search-box').addEventListener('input', function() {
    const query = this.value;
    const searchResults = document.getElementById('search-results');
    if (query.length > 0) {
        fetch(`/search/?q=${encodeURIComponent(query)}`) 
            .then(response => response.json())
            .then(data => {
                searchResults.innerHTML = '';
                data.forEach(stock => {
                    const div = document.createElement('div');
                    div.textContent = `${stock.Ticker} - ${stock.Name}`;
                    div.classList.add('stock-item'); 
                    div.dataset.symbol = stock.Ticker; 
                    div.addEventListener('click', () => {
                        fetchStockDetail(stock.Ticker); 
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

