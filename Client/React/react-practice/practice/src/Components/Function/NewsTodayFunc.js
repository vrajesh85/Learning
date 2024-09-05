import { useState , useEffect } from "react";

const NewsTodayFunc = () => {
    const APIKEY = "f7cf2468a6c940dfb39ac808cf99d0d1";
    const [news, setNews] = useState([]);

    useEffect(() => {
        const url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=";
        fetch(`${url}${APIKEY}`)
            .then(response => response.json())
            .then(data => setNews(data.articles))
            .catch((error) => console.error(error));
    },[]);

    const newsToday = news.map((article) => {
       return(
        <p>
            {article.title}
        </p>
       );
    });

    return(         
        <>
            {newsToday}
        </>
    );
};

export default NewsTodayFunc;