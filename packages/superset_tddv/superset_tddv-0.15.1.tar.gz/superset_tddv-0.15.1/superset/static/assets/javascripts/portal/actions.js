import shortid from 'shortid';
import { now } from '../modules/dates';
const $ = require('jquery');

export const RESET_STATE = 'RESET_STATE';

export function resetState() {
  return { type: RESET_STATE };
}
