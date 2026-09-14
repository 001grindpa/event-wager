def test_early_resolve_cannot_close_wager(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    contract = direct_deploy("contracts/EventWager.py")

    direct_vm.sender = direct_alice
    wager_id = contract.create_wager(
        "Did team X win on 2026-12-31?",
        "2026-12-31",
        "2026-12-31",
        "YES",
        "https://www.bbc.com/sport",
        "https://www.reuters.com/sports/",
        value=10**18,
    )

    with direct_vm.prank(direct_bob):
        contract.join(wager_id, value=10**18)

    wager = contract.get_wager(wager_id)
    assert "MATCHED" in wager

    with direct_vm.expect_revert("wager cannot be closed before resolve_after"):
        contract.resolve(wager_id)

    wager_after = contract.get_wager(wager_id)
    assert "MATCHED" in wager_after
    assert "REFUNDED" not in wager_after
    assert "SETTLED" not in wager_after

    status = contract.can_resolve(wager_id)
    assert "false" in status.lower() or '"allowed": false' in status.replace(" ", "")