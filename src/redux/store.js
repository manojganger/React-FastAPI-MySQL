// src/redux/store.js
import { createStore } from 'redux';

const initialState = {
  users: [],
};

function reducer(state = initialState, action) {
  switch (action.type) {
    case 'SET_USERS':
      return { ...state, users: action.payload };
    default:
      return state;
  }
}

const store = createStore(reducer);

export default store;
