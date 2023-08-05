/*
 * (C) Copyright 2016 Hewlett Packard Enterprise Development LP
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
package monasca.api.domain.model.notificationmethod;
 
import java.util.List;

import monasca.api.domain.model.common.Link;
import monasca.api.domain.model.common.Linked;
import monasca.common.model.domain.common.AbstractEntity;

public class NotificationMethodType extends AbstractEntity{

  private String type;


public NotificationMethodType() {
}

public NotificationMethodType(String type) {
  this.type = type.toUpperCase();
}

public String getType() {
  return type;
}

public void setType(String type) {
  this.type = type;
}

public String getId() {return type;} 

@Override
public int hashCode() {
  final int prime = 31;
  int result = super.hashCode();
  result = prime * result + ((type == null) ? 0 : type.hashCode());
  return result;
}

@Override
public boolean equals(Object obj) {
  if (this == obj)
    return true;
  if (!super.equals(obj))
    return false;
  if (getClass() != obj.getClass())
    return false;
  NotificationMethodType other = (NotificationMethodType) obj;
  if (type == null) {
     if (other.type != null)
       return false;
  } else if (!type.equals(other.type))
       return false;
  return true;
}


}