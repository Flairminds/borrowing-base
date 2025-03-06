import { configureStore } from '@reduxjs/toolkit';
import BaseFileDataSlice from './slices/baseFileData';

export const store = configureStore({
	reducer: {
		baseFileData: BaseFileDataSlice
	}
});