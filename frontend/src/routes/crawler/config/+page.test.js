import { render, fireEvent } from '@testing-library/svelte';
import Page from './+page.svelte';
import { goto } from '$app/navigation';
import { describe, expect, test, vi } from 'vitest';

/*
  * fireEvent: simulates user interactions like typing or clicking
  * render: puts components into the DOM for testing
  * vi: is verson of jest in vitest
*/

// Mocks the goto function
vi.mock('$app/navigation', () => ({
  goto: vi.fn()
}));

describe('Crawler Config Page', () => {
  test('submits form with valid data and navigates to next page', async () => {
    const { getByLabelText, getByRole } = render(Page);

    // Fill in required input
    const targetInput = getByLabelText('Target URL');
    await fireEvent.input(targetInput, { target: { value: 'https://juice-shop.herokuapp.com' } });

    // Submit the form
    const submitButton = getByRole('button', { name: /submit/i });
    await fireEvent.click(submitButton);

    // Assert redirect
    expect(goto).toHaveBeenCalledWith('/crawler/run', { replaceState: true });
  });
});
