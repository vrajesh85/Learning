import { useState } from "react";
import ChildFunction from "./ChildFunction";

const ParentFunction = () => {

    const [someValue, setSomeValue] = useState("Rajesh");

    const changeValue = (valueSent) => {
        setSomeValue(valueSent == "" ? "Rajesh" : valueSent)
    }

    return (
        <>
            Enter some value : <input type="text" placeholder="somevalue.." onChange={(e) => changeValue(e.target.value)}></input>
            <ChildFunction name={someValue}></ChildFunction>
        </>
    )
}

export default ParentFunction;