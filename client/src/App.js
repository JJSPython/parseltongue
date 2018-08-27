import React from 'react';

import Header from './components/Header';
import Footer from './components/Footer';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      html: '',
      text: '',
      textRepeats: '',
      table: '',
      json: '',
    };
  }

  handleChange = ({ target: { name, value } }) => {
    this.setState({ [name]: value });
  };

  handleSubmit = e => {
    e.preventDefault();
    console.log('Submiting the form'); // eslint-disable-line
    const api = 'https://vast-refuge-25114.herokuapp.com/setting';
    fetch(api, {
      method: 'POST',
    })
      .then(json => json())
      .then(result => console.log(result));
  };

  render() {
    const { html, text, textRepeats, table, json } = this.state;

    return (
      <div className="container">
        <div className="inner">
          <Header />
          <main>
            <form onSubmit={this.handleSubmit}>
              <div className="form-wrapper">
                <div className="form-group">
                  <label htmlFor="html">HTML 標籤</label>
                  <input
                    id="html"
                    className="input"
                    type="text"
                    name="html"
                    value={html}
                    onChange={this.handleChange}
                    placeholder="<h1></h1>"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="text">文字</label>
                  <input
                    id="text"
                    className="input"
                    type="text"
                    name="text"
                    value={text}
                    onChange={this.handleChange}
                    placeholder="text content"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="text-repeats">重覆的文字</label>
                  <input
                    id="text-repeats"
                    className="input"
                    type="text"
                    name="text-repeats"
                    value={textRepeats}
                    onChange={this.handleChange}
                    placeholder="{ 'search terms': 2 }"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="table">表格標題</label>
                  <input
                    id="table"
                    className="input"
                    type="text"
                    name="table"
                    value={table}
                    onChange={this.handleChange}
                    placeholder="table title"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="json">JSON 格式</label>
                  <input
                    id="json"
                    className="input"
                    type="text"
                    name="json"
                    value={json}
                    onChange={this.handleChange}
                    placeholder="{ key: { key: value } }"
                  />
                </div>
              </div>

              <div className="submit">
                <button>Parse it!</button>
              </div>
            </form>
          </main>
        </div>
        <Footer />
      </div>
    );
  }
}

export default App;
