<table class="styled">
    <thead>
        <tr>
            <th>{{name}}'s List of Friends</th>
        </tr>
    </thead>
    <tbody>
            % for instance in friendlist:
                <!-- Each row is a link to each individual friend chat-->
                <tr>
                    <td>{{instance}}</td>
                </tr>
            % end
    </tbody>
</table>

<p>Enter friend's name you want to select below!</p>
<p>
<form action="/friendlist" method="post">
    Friend Name: <input name="friendname" type="text" />
</br>
    <input value="Choose Friend" type="submit" />
</form>
</p>
</center>