import  * as React from 'react';
import './parameter.scss'
import { Draggable } from 'react-beautiful-dnd';

export interface IParameterSettings {
  id:string
  title:string
  type:string
}

interface IProps {
  initialSettings:IParameterSettings
  index:number
}

type IState = IParameterSettings

export class Parameter extends React.Component<IProps, IState> {

  public state:IState = {
    ...this.props.initialSettings // Initialze initial state props
  }

  public render() {
    return (
      <Draggable draggableId={`${this.state.id}`} index={this.props.index}>
        {(provided) => (

          <div className="component-parameter" ref={provided.innerRef}
            {...provided.draggableProps}
            {...provided.dragHandleProps}>
            {this.state.type} {this.state.title}
            
          </div>
        )}
      </Draggable>
    )
  }
}
