import { useState } from "react";

const NewsFeed = () => {

    // const[date, setState] = useState(new Date(),);
    // const[headlines, setHeadlines] = useState([]);

    const[state , setState] = useState({
        date : new Date(),
        headlines : []
    });

    const updateState = () => {
        setState(new Date());
    }
            
    return(
    <>
        <h1>
            The date is {state.date.toLocaleString()} and headlines are {state.headlines}
        </h1>
    </>
    );
};  

export default NewsFeed;