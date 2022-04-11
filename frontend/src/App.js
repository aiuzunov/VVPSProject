import React, { Component } from "react";
import axios from "axios";
import './App.css';
import $ from 'jquery';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      viewTab: 1,
      resultData: [],
      showSpinner: false,
      modal: false,
      selectedFile: null,
      errorMessage: null,
    };
  }

  componentDidMount() {
  }

  toggle = () => {
    this.setState({ modal: !this.state.modal });
  };

  displayTab = (status) => {
    return this.setState({ viewTab: status });
  };

  onFileChange = event => {
    this.setState({ selectedFile: event.target.files[0] });
  };

  onFileUpload = () => {
    if(!this.state.selectedFile)
    {
      return;
    }

    this.setState({ showSpinner: true });

    const formData = new FormData();

    formData.append('title',this.state.selectedFile.name);
    formData.append('file',this.state.selectedFile);

    var self = this;
    axios.post("api/upload", formData).then(function (res) {
        self.setState({ resultData: res.data, showSpinner: false });
    }).catch(function (error) {
         if(error.response.status >= 452 && error.response.status <= 499){
                self.setState({ errorMessage: error.response.statusText, showSpinner: false });
         }
    });
  };

  fileData = () => {
    if (this.state.selectedFile) {
      $('#submitFile').show();
      return (
        <div>
          <h2>Детайли за файла:</h2>
          <p>Име на файла: {this.state.selectedFile.name}</p>
          <p>Тип на файла: {this.state.selectedFile.type}</p>
          <p>
              Последно обновен:{" "}
              {this.state.selectedFile.lastModifiedDate.toDateString()}
          </p>
        </div>
      );
    }
    else
    {
      $('#submitFile').hide();
    }
  };

  renderFileUploader = () => {
    return (
        <div>
            <div className="mb-2">
                <div>
                    <label className="form-label">Моля, изберете файл:</label>
                </div>
                <label className="file-uploader" htmlFor="formFile">Избери файл</label>
                <input hidden id="formFile" className="form-control " type="file" onChange={this.onFileChange} />
             </div>
             <div>
                <button
                  id="submitFile"
                  className="hidden mb-3 btn btn-success"
                  onClick={this.onFileUpload}
                >
                  Качване на файл
                </button>
            </div>
          {this.fileData()}
        </div>
     );
  };

  renderFrequenciesTable = () => {
    return (
            <table className="table">
                <thead>
                    <tr>
                        <th className="text-center" scope="col"> ID на потребител </th>
                        <th className="text-center" scope="col"> Абсолютна честота </th>
                        <th className="text-center" scope="col"> Относителна честота </th>
                    </tr>
                </thead>
                <tbody>
                    {this.renderAbsoluteFreqItems()}
                </tbody>
            </table>
    );
  }

  renderTabList = () => {
    if(Object.keys(this.state.resultData).length === 0 || this.state.showSpinner === true)
    {
        return;
    }
    return (
    <div>
          <div className="nav nav-tabs">
            <span
              onClick={() => this.displayTab(1)}
              className={this.state.viewTab === 1 ? "nav-link active" : "nav-link"}
            >
              Абсолютна и относителната честота
            </span>
            <span
              onClick={() => this.displayTab(2)}
              className={this.state.viewTab === 2 ? "nav-link active" : "nav-link"}
            >
              Мода
            </span>
            <span
              onClick={() => this.displayTab(3)}
              className={this.state.viewTab === 3 ? "nav-link active" : "nav-link"}
            >
              Стандартно отклонение
            </span>
          </div>
          {this.state.viewTab === 1 ?
          this.renderFrequenciesTable() : <div></div>}
          {this.state.viewTab === 2 ?
          this.renderModesTable() : <div></div>}
          {this.state.viewTab === 3 ?
          this.renderStandardDeviationTable() : <div></div>}
      </div>
    );
  };

   renderModesTable = () => {
    return (
            <table className="table">
                <thead>
                    <tr>
                        <th className="text-center" scope="col"> Мода </th>
                    </tr>
                </thead>
                <tbody>
                    {this.renderModes()}
                </tbody>
            </table>
    );
  };


  renderStandardDeviationTable = () => {
    return (
            <table className="table">
                <thead>
                    <tr>
                        <th className="text-center" scope="col">  Стандартно отклонение </th>
                    </tr>
                </thead>
                <tbody>
                    {this.renderStandardDeviation()}
                </tbody>
            </table>
    );
  };

  renderStandardDeviation = () =>
  {
    if(this.state.resultData.standard_deviation === 'null')
    {
        return;
    }

    const standard_deviation = this.state.resultData.standard_deviation;

    return (
      <tr key={standard_deviation}>
        <td className="text-center"> {standard_deviation} </td>
      </tr>
    );
  };

  renderSpinner = () =>
  {
    if(!this.state.showSpinner)
    {
        return;
    }
    return(
        <center>
            <div className="spinner-border text-light" role="status">
                <span className="sr-only">Loading...</span>
            </div>
        </center>

    );
  };

  renderModes = () =>
  {
    if(!this.state.resultData.modes)
    {
        return;
    }

    const modes = this.state.resultData.modes;

    return modes.map((mode) => (
      <tr key={mode}>
        <td className="text-center"> {mode} </td>
      </tr>
    ));
  };

  renderAbsoluteFreqItems = () => {
    if(!this.state.resultData.frequencies)
    {
        return;
    }
    const newItems = Object.entries(this.state.resultData.frequencies);

    return newItems.map((item) => (
      <tr key={item[0]}>
        <td className="text-center"> {item[0]} </td>
        <td className="text-center"> {item[1][0]} </td>
        <td className="text-center"> {item[1][1]} </td>
      </tr>
    ));
  };

  render() {
    return (
      <main className="container">
        <h1 className="text-white text-uppercase text-center my-4">Проект по ВВПС</h1>
        <div className="row">
          <div className="col-md-7 col-sm-10 mx-auto p-0">
            <div className="card p-3">
              <div className="mb-1">
               {this.renderFileUploader()}
              </div>
              {this.state.errorMessage && (
                <div class="alert alert-danger">
                  <strong>Error!</strong> {this.state.errorMessage} 😭
                </div>
              )}
              { this.renderSpinner()}
              { this.renderTabList()}
            </div>
          </div>
        </div>
      </main>
    );
  }
}

export default App;