import { Component } from "react";

class NewsToday extends Component {
    

    constructor(props){
        super(props);
        this.APIKEY = "f7cf2468a6c940dfb39ac808cf99d0d1";
        this.state = {
            news:[]
        }
    }

    componentDidMount(){
        const url = `https://newsapi.org/v2/top-headlines?country=in&apiKey=${this.APIKEY   }`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                this.setState({
                    news : data.articles
                })
            })
            .catch(error => console.error(error));
    }

    render(){
        const newsToday = this.state.news.map((article) => {
            return (
                <p>
                    {article.title}
                </p>
            )
        });

        return(
            <>
                <h1> News Today</h1>
                    {newsToday}
            </>
        );
    }

}

export default NewsToday;