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

document.addEventListener('DOMContentLoaded', function () {
    const path = window.location.pathname;
    const symbol = path.substring(1); 
    if (symbol) {
        fetchStockDetail(symbol); 
    }
    document.getElementById('search-results').addEventListener('click', function (event) {
        if (event.target && event.target.classList.contains('stock-item')) {
            const symbol = event.target.dataset.symbol; 
            fetchStockDetail(symbol);
            setInterval(() => fetchStockDetail(symbol), 60000);
            window.location.href = `/${symbol}/profile/`;
        }
    });
});

function fetchStockDetail(symbol) {
    fetch(`/${symbol}`) 
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                displayStockDetail(data);
            }
        })
        .catch(error => {
            console.error('Lỗi khi lấy thông tin chi tiết:', error);
        });
}

function displayStockDetail(data) {
    document.getElementById('company-name').textContent = data.name || 'Unknown Company'; 
    document.getElementById('close-price').textContent = data.close || 'N/A'; 
    document.getElementById('stock-symbol').textContent = data.symbol; 
}