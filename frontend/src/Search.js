import React, { Component } from 'react'
import './search.css';
import { Link } from 'react-router-dom'
class Search extends Component {
    constructor(props) {
        super(props);
        this.state = {
            query: ''
        };
        this.updateQuery = this.updateQuery.bind(this);
        this.handleQueryChange = this.handleQueryChange.bind(this);

    }
    async updateQuery(e) {
        this.setState({ query: e.target.value })
    }
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

    render() {
        let body = null;
        body = (
            <header className="clssearch-container">
                <div>
                    <h1 className="clssearch-header">
                        COMBIN-ING
                    </h1>

                    <div className="clssearch-box">
                        <input
                            placeholder='Search Ingredients ...'
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

            </header>

        )

        var error = null;

        return (
            <div >
                {error}
                <div className="clssearch-container">

                    {body}
                </div>
            </div>
        );
    }

}
export default Search;