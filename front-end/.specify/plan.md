# Implementation Plan: ShowMe AI Ticket Search

**Branch**: `001-ticket-search-ui` | **Date**: 2025-12-06 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `.specify/spec.md`

## Summary

AI-powered ticket search frontend with 4-step onboarding flow, event results view sorted by price/distance, and interactive seat map viewer. Built with React + Vite, styled with Tailwind CSS + shadcn/ui.

## Technical Context

**Language/Version**: TypeScript 5.x  
**Framework**: React 19 + Vite 7  
**UI Library**: Tailwind CSS 3.x + shadcn/ui  
**State Management**: React Context + useReducer (keep it simple)  
**Testing**: Vitest + React Testing Library  
**Target Platform**: Modern browsers (Chrome, Safari, Firefox, Edge)  
**Performance Goals**: 60fps interactions, <3s initial load, <2s search results  
**Constraints**: Mobile-first responsive design, offline-capable search criteria storage  
**Scale/Scope**: Single-page app, 5 main views

## Constitution Check

*GATE: Must pass before implementation.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Radical Simplicity | ✅ | No state management library, minimal dependencies |
| Test-Driven Development | ✅ | Vitest + RTL, tests written before implementation |
| Clean Architecture | ✅ | Domain/Application/Infrastructure separation |

## Project Structure

```text
front-end/
├── src/
│   ├── domain/           # Business logic (no React)
│   │   ├── entities/
│   │   └── services/
│   ├── application/      # Use cases (hooks)
│   ├── infrastructure/   # API + storage
│   ├── components/       # UI components
│   │   ├── ui/          # shadcn primitives
│   │   ├── onboarding/
│   │   ├── results/
│   │   └── seatmap/
│   └── pages/           # Route components
└── tests/
    ├── unit/
    └── integration/
```

## Dependencies

- react, react-dom, react-router-dom
- tailwindcss, shadcn/ui components
- vitest, @testing-library/react, jsdom
