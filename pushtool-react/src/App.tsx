import * as React from 'react';
import './App.css';
import { Bank, IBankConfig } from "./components";
import { DragDropContext, DropResult, Droppable } from 'react-beautiful-dnd';
import update from "immutability-helper";

interface IState {
  banks:IBankConfig[]
}

class App extends React.Component<{}, IState> {

  public state:IState = {
    banks: [
      { id: "Bank one", name: "Hello", parameters: [
        { title:"VCF", type: "knob", id:"1" },
        { title:"Test", type: "knob", id:"2" },
        { title:"Hello", type: "Hi", id:"3"},
      ]},
      { id: "Bank two", name: "Bank two", parameters: [
        { title:"VCF", type: "knob", id:"4" },
        { title:"Test", type: "knob", id:"5" },
        { title:"Hello", type: "Hi", id:"6"},
      ]}
    ]

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
            </div>
          )}
        </Droppable>
      </DragDropContext>
    );
  }

  private getBanks() {
    return this.state.banks.map((value, key) => <Bank index={key}   key={value.id} initialBankConfig={value} />)
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

    this.setState({
      banks: newState
    });
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

    this.setState({
      banks: newState
    });
  }
}

export default App;
