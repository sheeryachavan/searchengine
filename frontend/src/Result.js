import React, { Component } from 'react';
import { Link } from 'react-router-dom'
import APIClient from './apiClient'
import './search.css';
import ovenLoad from './images/oven.gif';
class Result extends Component {
    constructor(props) {
        super(props);
        this.state = {
            list: [],
            loading: false,
            query: "",
            error: ""
        };
        this.handleQueryChange = this.handleQueryChange.bind(this);
    }
    // componentWillReceiveProps(nextProps, nextState) {
    //     this.getResults()
    // }
    handleQueryChange = query => {
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
                this.setState({ loading: true })
                this.apiClient.getResults(this.props.location.query.query).then((data) => {
                    if (data.error) {

                        this.setState({ ...this.state, error: data.error, loading: false, query: this.props.location.query.query,error:"" })
                    }
                    else
                        this.setState({ ...this.state, list: data, loading: false, query: this.props.location.query.query })
                }
                );
            }
            else {
                var link = document.getElementById('resulttest1');
                link.click();
            }

        }
        catch (e) {
            console.log(e);
            this.setState({ loading: true });
        }

    }
    async reloadResults() {
        try {

            this.apiClient = new APIClient();
            if (this.state.query) {
                this.setState({ loading: true })
                this.apiClient.getResults(this.state.query).then((data) => {
                    if (data.error)
                        this.setState({ ...this.state, error: data.error, loading: false, query: this.state.query })
                    else
                        this.setState({ ...this.state, list: data, loading: false, query: this.state.query ,error:""})
                }
                );
            }
            else {
                var link = document.getElementById('resulttest1');
                link.click();
            }

        }
        catch (e) {
            console.log(e);
            this.setState({ loading: true });
        }
    }

    render() {
        let body = null;
        let searchlist = null;
        var items = null;
        if (this.state.list.length === 0 && this.state.loading) {
            items =
                <div>
                    <h1>Enjoy the Aroma! The chefs are working for you...</h1>
                    <br />
                    <img alt="Oven" height="500" width="500" src={ovenLoad} />
                </div>
        }
        else if (this.state.list.length > 0 && this.state.error === "") {
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
        else if (this.state.error !== "") {
            debugger;
            items = <div><h1>{this.state.error}</h1></div>
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
                                this.reloadResults()
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
                    pathname: "/", query: {
                        query: this.state.query
                    }
                }} style={{ hidden: true }} id="resulttest1">
                </Link>
                <h2> Search results for : {this.state.query}</h2>
                <hr />
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