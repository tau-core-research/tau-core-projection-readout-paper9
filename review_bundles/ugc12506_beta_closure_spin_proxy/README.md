# UGC12506 Beta-Closure Spin Proxy Review Prompt

You are reviewing a residual-blind source-proxy gate, not an endpoint result.

Please decide whether any residual-blind spin/envelope normalization route can be carried as a caveated transfer-review input for beta_cl preflight. Do not use rotation-curve residuals, endpoint RMSE, baseline ranks, wrong-family Tau scores, or post-hoc amplitude changes.

Review objects:

`lambda_spin_proxy = lambda_ref * (1 + 0.35 extent_load + 0.25 velocity_load + 0.25 gas_load + 0.15 edgeon_load)`

with `lambda_ref = 0.10`. The loads use source-side `RHI/Rdisk`, `Vflat`, H I mass, and inclination only.

and the conservative Bullock-like disk-inferred conversion control:

`lambda'_disk = (2 Rdisk Vflat) / (sqrt(2) R200 V200)`, with `R200 = V200/(10 H0)`.

Key decisions:

1. Are the source fields acceptable for a spin/envelope exposure proxy?
2. Should the exposure proxy, Bullock-like conversion proxy, direct-source route, or a new residual-blind rule be used?
3. Do you agree that the Marr (2015) NGC7331 disc-spin lambda is source context only and cannot directly fill the beta_cl halo/envelope lambda_spin slot without a conversion rule?
4. Which transfer targets, if any, may carry the proxy as caveated inputs?

Fill `response/ugc12506_beta_closure_spin_proxy_review_response_blank.csv` and leave `endpoint_scores_allowed=false` unless a separate future endpoint manifest is built after this review.
