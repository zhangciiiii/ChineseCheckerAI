- The old versioned horizon_count is better.
- This version takes into account the "stuck" situation, and correct some errors concerning depth.
- 大多数时候深度都保持在2，但多数时候memory不会超过30。
- 明天我们将研究，深度故意调高，memory故意调小，以及horizon_count占比问题。
- 我们希望还是可以跳出只和marblefish()作对比的情况，来重新审视我们的defAction()函数。
