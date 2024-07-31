document.addEventListener('DOMContentLoaded', function() {
    fetch('http://localhost:5000/api/news')
        .then(response => response.json())
        .then(data => {
            const newsContainer = document.getElementById('news-container');
            if (data.length === 0) {
                const noNewsMessage = document.createElement('p');
                noNewsMessage.textContent = 'No news available at the moment.';
                newsContainer.appendChild(noNewsMessage);
            } else {
                data.forEach(news => {
                    const newsItem = document.createElement('div');
                    newsItem.className = 'news-item';

                    const sourceLink = document.createElement('a');
                    sourceLink.href = `/${news.source_type.toLowerCase()}/${news.source_id}`;
                    sourceLink.textContent = `${news.source_type}: ${news.source_name}`;

                    const tags = document.createElement('div');
                    tags.className = 'tags';
                    news.tags.forEach(tag => {
                        const tagElement = document.createElement('span');
                        tagElement.className = 'tag';
                        tagElement.textContent = tag;
                        tags.appendChild(tagElement);
                    });

                    newsItem.appendChild(sourceLink);
                    newsItem.appendChild(tags);
                    newsContainer.appendChild(newsItem);
                });
            }
        })
        .catch(error => {
            const newsContainer = document.getElementById('news-container');
            const errorMessage = document.createElement('p');
            errorMessage.textContent = 'Failed to load news. Please try again later.';
            newsContainer.appendChild(errorMessage);
            console.error('Error loading news:', error);
        });
});
