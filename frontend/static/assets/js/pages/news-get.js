document.addEventListener('DOMContentLoaded', function() {
    fetch('http://localhost:5000/api/news')
        .then(response => response.json())
        .then(data => {
            const newsContainer = document.getElementById('news-container');
            if (data.data.length === 0) {
                const noNewsMessage = document.createElement('p');
                noNewsMessage.textContent = 'No news available at the moment.';
                newsContainer.appendChild(noNewsMessage);
            } else {
                data.data.forEach(news => {
                    const card = document.createElement('div');
                    card.className = 'card';

                    const cardHeader = document.createElement('div');
                    cardHeader.className = 'card-header';

                    const cardHeaderText = document.createElement('h5');
                    cardHeaderText.textContent = news.title;  // Adjust this based on what you need

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
                        console.log(tag);
                    });

                    cardHeader.appendChild(cardHeaderText);

                    const cardBody = document.createElement('div');
                    cardBody.className = 'card-body';

                    const cardBodyText = document.createElement('p');
                    cardBodyText.textContent = news.body;

                    cardBody.appendChild(cardBodyText);
                    cardBody.appendChild(sourceLink);
                    cardBody.appendChild(tags);

                    card.appendChild(cardHeader);
                    card.appendChild(cardBody);

                    newsContainer.appendChild(card);
                });
            }
        })
        .catch(error => {
            const newsContainer = document.getElementById('news-container');

            const card = document.createElement('div');
            card.className = 'card';

            const cardHeader = document.createElement('div');
            cardHeader.className = 'card-header';

            const cardHeaderText = document.createElement('h5');
            cardHeaderText.textContent = 'Failed to fetch news';

            const cardBody = document.createElement('div');
            cardBody.className = 'card-body';

            const cardBodyText = document.createElement('p');
            cardBodyText.textContent = 'Something went wrong. Check the API.';

            cardHeader.appendChild(cardHeaderText);
            cardBody.appendChild(cardBodyText);

            card.appendChild(cardHeader);
            card.appendChild(cardBody);

            newsContainer.appendChild(card);

            console.error('Error loading news:', error);
        });
});