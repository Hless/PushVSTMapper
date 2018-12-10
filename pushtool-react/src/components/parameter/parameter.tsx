import  * as React from 'react';
import './parameter.scss'
import { Draggable } from 'react-beautiful-dnd';
import { InlineInput } from "../inline-input/inline-input";
import update from "immutability-helper";

import { ParameterDial } from "../parameter-dial/parameter-dial";

export interface IParameterSettings {
  id:string
  title:string
  type:"option"|"switch"|"dial"
  value:string
}

interface IProps {
  config:IParameterSettings
  index:number,
  update: (settings:IParameterSettings) => void
  editable:boolean
}


export class Parameter extends React.Component<IProps> {

  public render() {
    return (
      <Draggable draggableId={`${this.props.config.id}`} index={this.props.index}>
        {(provided) => (

          <div id={'parameter-' + this.props.config.id} className="component-parameter" ref={provided.innerRef}
            {...provided.draggableProps}
            {...provided.dragHandleProps}>

            {this.titleField()}
            <div className="visual">
              {this.parameterDisplay()}
            </div>

          </div>
        )}
      </Draggable>
    )
  }

  public titleField = () => {
    if(this.props.editable)
      return <InlineInput defaultValue={this.props.config.title} onUpdate={this.onTitleUpdated} />
    else
      return <h5>{this.props.config.title}</h5>
  }
  
  public parameterDisplay = () => {
    switch(this.props.config.type) {
      case "dial":
        return <ParameterDial value={this.props.config.value} />;
      case "option":
        return;
      case "switch":
        return;
    }
    return "Unknown"
  }

  public onTitleUpdated = (value:string) => {
      this.props.update(update(this.props.config, {
        title: {
          $set: value
        }
      }))
  }
}
