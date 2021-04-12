// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

contract transferMoney{
function buyProperty(address payable owner_id, uint value) public payable{
    owner_id.transfer(value);
  
    }
}