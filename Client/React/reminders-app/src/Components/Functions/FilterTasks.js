import { PropTypes } from "prop-types";

const FilterTasks = (props) => {

    const handleOnChange = (e) => {
        props.setSelectedFilter(e.target.value);
    };

    return(
        <>
            <label htmlFor="filterReminders">Show Tasks Due :    
            <select id="filterReminders" value={props.selectedFilter} onChange={handleOnChange}>
                <option value="2day">within 2 days </option>
                <option value="1week">Within 1 week</option>
                <option value="30days">Within 30 days</option>
                <option value="all">Any time</option>
            </select>  
            </label>               
        </>
    );
};

FilterTasks.propTypes = {
    selectedFilter : PropTypes.string,
    setSelectedFilter : PropTypes.func
};

FilterTasks.defaultProps = {
    selectedFilter : 'all'
};

export default FilterTasks;