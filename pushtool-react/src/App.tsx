import "@fortawesome/fontawesome-pro/css/all.min.css";

import * as React from 'react';
import './App.css';

import { Bank, IBankConfig, BankUpdateEvent, IParameterSettings } from "./components";
import { AvailableParameters } from "./components/available-parameters/available-parameters";
import { DragDropContext, DropResult, Droppable } from 'react-beautiful-dnd';
import update from "immutability-helper";

import mockedBanks from "./mock/banks";
import mockedAvailableParams from "./mock/available";


interface IState {
  banks:IBankConfig[],
  available:IParameterSettings[]
}


class App extends React.Component<{}, IState> {

  public activeConfig = localStorage.getItem("_active_bank");

  public state:IState = {
    banks: this.activeConfig ? JSON.parse(this.activeConfig) : mockedBanks,
    available: mockedAvailableParams
  };

  /*
  public componentDidMount() {
    setTimeout(() => {
      this.setState({
        bankRows: [...this.state.bankRows, "Value 7"]
      })
    }, 5000)
  }*/

  public render() {
    return (
      <DragDropContext onDragEnd={this.onDragEnd}>
        <Droppable droppableId="banksDroppable">
          {(provided ) => (
            <div className="App" ref={provided.innerRef}>
              <div className="banks">
                {this.getBanks()}
              </div>
              <AvailableParameters parameters={this.state.available} />
            </div>
          )}
        </Droppable>
      </DragDropContext>
    );
  }

  private getBanks() {
    return this.state.banks.map((value, key) => <Bank
      index={key}
      key={value.id}
      config={value}
      update={this.bankUpdate} />)
  }

  private updateBanks(bankConfig:IBankConfig[]) {

    localStorage.setItem("_active_bank", JSON.stringify(bankConfig));
    // Persist bank state
    this.setState({
      banks: bankConfig
    })
  }

  private bankUpdate = (event:BankUpdateEvent) => {
    const bank = this.state.banks.findIndex((value) => value.id === event.id);

    let newState = this.state.banks;
    if(event.changes.name) {
      newState = update(newState, {
        [bank]: {
         name: { $set: event.changes.name }
        }
      });
    }

    if(event.changes.parameter) {
      const bankValue = this.state.banks.find((value) => value.id === event.id);

      const param = bankValue!.parameters.findIndex((p) => p.id === event.changes.parameter!.id)
      newState = update(newState, {
        [bank]: {
          parameters: {
            [param]: {
              $set: event.changes.parameter!
            }
          }
        }
      });
    }

    this.updateBanks(newState);
  }



  private onDragEnd = (value:DropResult) => {
    if(!value.destination)
      return;

    if(value.destination.droppableId === "banksDroppable")
      this.moveBank(value);
    else
      this.moveParameter(value);
  };

  private moveBank(value:DropResult) {
    const bank = this.state.banks.find((_, key:number) => key === value.source.index);

    let newState = update(this.state.banks, {
      $splice: [[value.source.index, 1]]
    });

    newState = update(newState, {
      $splice: [[value.destination!.index, 0, bank!]]
    });

    this.updateBanks(newState);
  }

  private moveParameter(value:DropResult) {
    const from = this.state.banks.findIndex(bank => bank.id === value.source.droppableId);
    const to = this.state.banks.findIndex(bank => bank.id === value.destination!.droppableId);

    const fromBank = this.state.banks[from];

    const param = fromBank.parameters.find((_, key:number) => key === value.source.index);

    let newState = update(this.state.banks, {
      [from]: {
        parameters: {
          $splice: [[value.source.index, 1]]
        }
      }
    });

    newState = update(newState, {
      [to]: {
        parameters: {
          $splice: [[value.destination!.index, 0, param!]]
        }
      }
    })

    this.updateBanks(newState);
  }
}

export default App;
