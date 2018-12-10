import "@fortawesome/fontawesome-pro/css/all.min.css";

import * as React from 'react';

import * as ReactDOM from 'react-dom';

import './App.css';

import { Bank, IBankConfig, BankUpdateEvent, IParameterSettings } from "./components";
import { AvailableParameters } from "./components/available-parameters/available-parameters";
import { DragDropContext, DropResult, Droppable, DragUpdate } from 'react-beautiful-dnd';
import update from "immutability-helper";

import mockedBanks from "./mock/banks";
import mockedAvailableParams from "./mock/available";


interface IState {
  banks:IBankConfig[],
  available:IParameterSettings[]
}


class App extends React.Component<{}, IState> {

  public activeConfig = localStorage.getItem("_active_bank");

  private initialBanks:IBankConfig[] = this.activeConfig ? JSON.parse(this.activeConfig) : mockedBanks;
  private initialFlat:IParameterSettings[] = (this.initialBanks as any).reduce((previousValue:any[], currentValue:IBankConfig) =>{
    return [...previousValue, ...currentValue.parameters];
  }, []);

  public state:IState = {
    banks: this.initialBanks,
    available: mockedAvailableParams.filter((a) => !this.initialFlat.find((b) => b.id == a.id))
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
      <DragDropContext onDragEnd={this.onDragEnd} onDragUpdate={this.onDragUpdate}>
        <Droppable droppableId="banksDroppable">
          {(provided ) => (
            <div className="App" ref={provided.innerRef}>
              <div className="banks">
                {this.getBanks()}
              </div>
              {this.getAvailableParameters()}
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

  private getAvailableParameters() {
    const paramComponent = <AvailableParameters parameters={this.state.available} />;

    return paramComponent;
  }

  private updateBanks(bankConfig?:IBankConfig[], available?:IParameterSettings[]) {
    let stateUpdate:any = {};
    if(bankConfig) {
      localStorage.setItem("_active_bank", JSON.stringify(bankConfig));
      stateUpdate.banks = bankConfig;
    }

    if(available) {
      stateUpdate.available = available;
    }

    this.setState(stateUpdate)
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

    if(value.destination.droppableId === "banksDroppable") {
      this.moveBank(value);
    } else {
      this.moveParameter(value);
    }
  };

  private onDragUpdate = (update:DragUpdate) => {
    const c = (ReactDOM.findDOMNode(this) as Element).querySelector(`[id='parameter-${update.draggableId}']`);
    if(!c) return;
    const node:Element = c!;

    if(!update.destination || update.destination.droppableId === "availableParameters") {
      let className = node.className.replace(" expanded", "");
      className += " collapsed";
      node.className = className;

    } else {
      let className = node.className.replace(" collapsed", "");
      className += " expanded";
      node.className = className;
    }
  }

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

    let newState:IState;
    let param:IParameterSettings;
    if(value.source.droppableId !== "availableParameters") {
      // Find and remove paramater from bank
      const from = this.state.banks.findIndex(bank => bank.id === value.source.droppableId);
      const fromBank = this.state.banks[from];
      param = fromBank.parameters.find((_, key:number) => key === value.source.index)!;
      newState = update(this.state, {
        banks: {
         [from]: {
           parameters: {
             $splice: [[value.source.index, 1]]
           }
         }
        }
      });
    } else {

      // Find and remove parameter from available parameters
      param = this.state.available.find((_, key:number) => key === value.source.index)!;

      newState = update(this.state, {
         available: {
           $splice: [[value.source.index, 1]]
         }
      });
    }

    if(value.destination!.droppableId !== "availableParameters") {
      const to = this.state.banks.findIndex(bank => bank.id === value.destination!.droppableId);

      newState = update(newState!, {
        banks: {
          [to]: {
            parameters: {
              $splice: [[value.destination!.index, 0, param!]]
            }
          }
        }
      })
    } else {

      newState = update(newState!, {
         available: {
           $splice: [[value.destination!.index, 0, param!]]
         }
      });
    }

    this.updateBanks(newState.banks, newState.available);
  }
}

export default App;
