// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;
// import library file
import "./stringUtils.sol";
// struct properties{
//     string owner;
//     string prop_id;
//     string street;
//     string district;
//     string state;
//     bool availability;
//     bool requested;
//     string requester;
//   }
   
contract userRecords {
  // enum type variable to store user gender
  // enum genderType { male, female }
  // Actual user object which we will store
  
  struct properties{
    // user owner;
    address payable owner_id;
    string prop_id;
    string street;
    string district;
    string state;
    bool availability;
    bool requested;
    string requester;
    address requester_id;
    bool approved;
    uint value;
  }
  
  struct user{
    address payable user_id;
    string name;
    string aadhar_number;
    string pan_number;
    // properties[] property;
  }
  // user object
  user[] user_obj;
  properties[] property_list;
  //Internal function to conver genderType enum from string
  // function getGenderFromString(string memory gender) internal pure returns   (genderType) {
  //   if(StringUtils.equal(gender, "male")) {
  //     return genderType.male;
  //   } else {
  //     return genderType.female;
  //   }
  // }
  //Internal function to convert genderType enum to string
  // function getGenderToString(genderType gender) internal pure returns (string memory) {
  //   if(gender == genderType.male) {
  //     return "male";
  //   } else {
  //     return "female";
  //   }
  // }
  // set user public function
  // This is similar to persisting object in db.
  function setUser(address payable user_id,string memory name, string memory aadhar_number, string memory pan_number) public {
    // genderType gender_type = getGenderFromString(gender);
    user_obj.push(user({user_id: user_id,name:name, aadhar_number: aadhar_number, pan_number: pan_number}));
  }
  
  // get user public function
  // This is similar to getting object from db.
  function getUser() public view returns (user[] memory) {
    return (user_obj);
  }

  function addProperty(address payable owner_id, string memory prop_id, string memory street, string memory district, string memory state, uint value) public {
    property_list.push(properties({owner_id: owner_id, prop_id: prop_id, street: street, district: district, state: state, availability: false, requested: false, requester:"", requester_id: owner_id, approved: false, value: value}));
  }

  function getProperty() public view returns (properties[] memory) {
    return (property_list);
  }

  function setProperty(string memory prop_id) public {
    uint i;
    for (i = 0; i< property_list.length; i++){
      if (StringUtils.equal(property_list[i].prop_id,prop_id)){
        property_list[i].availability = true;
        break;
      }
    }
  }

  function requestProperty(address requester_id,string memory prop_id) public{
    uint i;
    uint j;

    for (i=0; i<property_list.length; i++){
      if (StringUtils.equal(property_list[i].prop_id,prop_id)){
        property_list[i].requested = true;
        property_list[i].availability = false;
        for (j=0; j<user_obj.length; j++){
          if (user_obj[j].user_id == requester_id){
          property_list[i].requester = user_obj[j].name;
          break;
          }
        }
        
        property_list[i].requester_id = requester_id;
        break;
      }
    }

  }

  function sellProperty(string memory prop_id) public {
    uint i;
    for (i=0; i<property_list.length; i++){
      if (StringUtils.equal(property_list[i].prop_id,prop_id)){
        property_list[i].approved = true;
        break;
      }
    }
    
  }

  function buyProperty(address payable owner_id, uint value) public {
    owner_id.transfer(value);
  
    }

  function updateProperty(string memory prop_id, address payable buyer ) public {
    uint i;
    for (i=0; i<property_list.length; i++){
      if (StringUtils.equal(property_list[i].prop_id,prop_id)){
        property_list[i].approved = false;
        property_list[i].availability = false;
        property_list[i].requested = false;
        property_list[i].owner_id = buyer;
        property_list[i].requester = "";
        property_list[i].requester_id = buyer;
        break;
      }
    }
  }


}