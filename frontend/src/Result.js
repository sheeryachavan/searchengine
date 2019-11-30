import React, { Component } from 'react';
import { Link } from 'react-router-dom'
import APIClient from './apiClient'
import './search.css';
class Result extends Component {
    constructor(props) {
        super(props);
        this.state = {
            list: [
                {
                    "_id": "5ddc406b1ced558962a44904",
                    "image": "http://fd2static.foodfood.com.s3.ap-south-1.amazonaws.com/images/Chicken-Farcha-84589.jpg",
                    "title": "Chicken Farcha",
                    "Prep": " 2 hours",
                    "Cook": " 30 minutes",
                    "key_ing": ["Chicken drumsticks", "Eggs", "Breadcrumbs"],
                    "desc": "A popular Parsi deep-fried chicken drumsticks ",
                    "link": "https://www.foodfood.com/recipedetails/chicken-farcha"
                },
                {
                    "_id": "5ddc406b1ced558962a44904",
                    "image": "http://fd2static.foodfood.com.s3.ap-south-1.amazonaws.com/images/Khatti-Mooli-2948.jpg",
                    "title": "Chicken Farcha",
                    "Prep": " 2 hours",
                    "Cook": " 30 minutes",
                    "key_ing": ["Chicken drumsticks", "Eggs", "Breadcrumbs"],
                    "desc": "A popular Parsi deep-fried chicken drumsticks ",
                    "link": "https://www.foodfood.com/recipedetails/chicken-farcha"
                },
                {
                    "_id": "5ddc406b1ced558962a44904",
                    "image": "http://fd2static.foodfood.com.s3.ap-south-1.amazonaws.com/images/Chicken-Farcha-84589.jpg",
                    "title": "Chicken Farcha",
                    "Prep": " 2 hours",
                    "Cook": " 30 minutes",
                    "key_ing": ["Chicken drumsticks", "Eggs", "Breadcrumbs"],
                    "desc": "A popular Parsi deep-fried chicken drumsticks ",
                    "link": "https://www.foodfood.com/recipedetails/chicken-farcha"
                },
                {
                    "_id": "5ddc406b1ced558962a44904",
                    "image": "http://fd2static.foodfood.com.s3.ap-south-1.amazonaws.com/images/Khatti-Mooli-2948.jpg",
                    "title": "Chicken Farcha",
                    "Prep": " 2 hours",
                    "Cook": " 30 minutes",
                    "key_ing": ["Chicken drumsticks", "Eggs", "Breadcrumbs"],
                    "desc": "A popular Parsi deep-fried chicken drumsticks ",
                    "link": "https://www.foodfood.com/recipedetails/chicken-farcha"
                },
                {
                    "_id": "5ddc406b1ced558962a44904",
                    "image": "http://fd2static.foodfood.com.s3.ap-south-1.amazonaws.com/images/Chicken-Farcha-84589.jpg",
                    "title": "Chicken Farcha",
                    "Prep": " 2 hours",
                    "Cook": " 30 minutes",
                    "key_ing": ["Chicken drumsticks", "Eggs", "Breadcrumbs"],
                    "desc": "A popular Parsi deep-fried chicken drumsticks ",
                    "link": "https://www.foodfood.com/recipedetails/chicken-farcha"
                },
                {
                    "_id": "5ddc406b1ced558962a44904",
                    "image": "http://fd2static.foodfood.com.s3.ap-south-1.amazonaws.com/images/Chicken-Farcha-84589.jpg",
                    "title": "Chicken Farcha",
                    "Prep": " 2 hours",
                    "Cook": " 30 minutes",
                    "key_ing": ["Chicken drumsticks", "Eggs", "Breadcrumbs"],
                    "desc": "A popular Parsi deep-fried chicken drumsticks ",
                    "link": "https://www.foodfood.com/recipedetails/chicken-farcha"
                }
            ]
        };
        this.handleQueryChange = this.handleQueryChange.bind(this);
    }
    // componentWillReceiveProps(nextProps, nextState) {
    //     this.getResults()
    // }
    handleQueryChange = query => {
        debugger;
        this.setState({
            query: query.target.value
        });
    };
    handleCloseClick = () => {
        this.setState({
            query: '',
        });
    };

    async componentDidMount() {
        try {
            this.apiClient = new APIClient();
            if (this.props.location && this.props.location.query.query) {
                this.apiClient.getResults(this.props.location.query.query).then((data) =>
                    this.setState({ ...this.state, list: data })
                );
            }

        }
        catch (e) {
            console.log(e)
        }

    }


    render() {
        let body = null;
        let searchlist = null;
        var items = null;
        if (this.state.list.length > 0) {
            items = this.state.list.map((item, key) =>

                <div className="carddisplay">

                    <a href={item.link} target="_blank">
                        <figure style={{ backgroundImage: `linear-gradient( rgba(0,0,0,.5), rgba(0,0,0,.5) ),url(${item.image})` }} className="figure">
                            <div class="date"><div>
                                <strong>Prep</strong>:{item.Prep}
                            </div>
                                <div>
                                    <strong>Cook</strong>:{item.Cook}
                                </div></div>
                            <figcaption>
                                <h4> <span>{item.title}</span></h4>
                                <p>{item.desc}</p>

                            </figcaption>
                        
                        </figure>
                    </a>

                    {/* <div>
                        <a href={item.link} className="clslistlink">{item.title}</a>

                    </div>
                    <div className="clsmainlink">www.foodfood.com</div>
                    <div className="clsdesc">{item.desc}</div> */}
                </div>);
        }
        else {
            items = <div><h1>Sorry! No Results Found</h1></div>
        }

        body = (
            <div>

                <div className="clssearch-boxrp">
                    <input
                        placeholder='Search Ingredients...'
                        className='clssearch-txt' value={this.state.query} onChange={this.handleQueryChange}
                        onKeyPress={(event) => {
                            if (event.key === 'Enter' || event.key === 'Return') {
                                var link = document.getElementById('resulttest');
                                link.click();
                            }
                        }}
                    />
                    <button
                        className="clssearch-boxClose"
                        onClick={this.handleCloseClick}
                    >
                        x
                </button>
                </div>
                <Link to={{
                    pathname: "/results", query: {
                        query: this.state.query
                    }
                }} style={{ hidden: true }} id="resulttest">
                </Link>
            </div >

        )

        var error = null;

        return (
            <div >
                {error}
                {body}
                {items}
            </div>
        );
    }

}
export default Result;